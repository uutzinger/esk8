#!/usr/bin/env python3
"""
Urs Utzinger
Fall 2023

Based on: 
"""

import argparse
import sys
import time

import odrive
from odrive.enums import *
from odrive.utils import set_motor_thermistor_coeffs, dump_errors

class MotorConfig:
    """
    Class for configuring an Odrive axis for a 
    192KV Turnigy SK8: 100A, 12cells, 4400W, 14 poles
    motor. Only works with one axis at a time.
    """

    # Motor
    # =====
    MOTOR_KV = 192.0 # kilo Volts
    # Estimated KV but should be measured using the "drill test", which can
    # be found here:
    # https://discourse.odriverobotics.com/t/project-hoverarm/441    
    MOTOR_POLES = 14 # Poles
    MOTOR_POLE_PAIRS = int(MOTOR_POLES / 2)    
    # Motor type
    MOTOR_TYPE = MOTOR_TYPE_HIGH_CURRENT

    # Min/Max phase inductance of motor
    MIN_PHASE_INDUCTANCE = 0
    MAX_PHASE_INDUCTANCE = 0.001

    # Min/Max phase resistance of motor
    MIN_PHASE_RESISTANCE = 0
    MAX_PHASE_RESISTANCE = 0.5

    # Brake resistor
    # ==============
    R_BREAK = 2.0 # Ohm
    # This is the resistance of the brake resistor. You can leave this
    # at the default setting if you are not using a brake resistor. Note
    # that there may be some extra resistance in your wiring and in the
    # screw terminals, so if you are getting issues while braking you may
    # want to increase this parameter by around 0.05 ohm.
    MAX_REGEN_CURRENT = -36.0 # Amps
    # This is the amount of current allowed to flow back into the power supply.
    # The convention is that it is negative. By default, it is set to a
    # conservative value of 10mA. If you are using a brake resistor and getting
    # DC_BUS_OVER_REGEN_CURRENT errors, raise it slightly. If you are not using
    # a brake resistor and you intend to send braking current back to the power
    # supply, set this to a safe level for your power source. Note that in that
    # case, it should be higher than your motor current limit + current limit
    # margin.
    
    # Current
    # =======
    # Current Limit = Motor Wattage / Battery Voltage
    # Turnigy: Limit = 4400W /13S (13*3.8) = 90A - 100A
    # 
    # 10A for safety, 60A default
    #
    # Use low value e.g. 20A to start with for calibration then set to 60A
    # For more than 60A, set the current range to higher value and reboot to take effect
    MOTOR_CURRENT_LIMIT = 20
    # current range > current_lim + current_lim_margin, but as low as possible
    CURRENT_RANGE = 60
    CURRENT_LIMIT_MARGIN = 16 # 10A default
    # Reduced bandwidth for high inductance motors
    CURRENT_CONTROL_BANDWIDTH = 100 # 100 default, 1000 for high power    
    CALIBRATION_CURRENT = 10 # 10A default, larger for larger motor
    # resistance_calib_max_voltage < 0.5 vbus_voltage
    # resistance_calib_max_voltage = calibration_current (10) * phase_resistance (0.04) 
    RESISTANCE_CALIBRATION_MAX_VOLTAGE = 5 
    
    # Encoder
    # =======
    ENCODER_MODE = ENCODER_MODE_HALL
    # Since the hall feedback only has 42 counts per revolution, we want to
    # reduce the velocity tracking bandwidth to get smoother velocity
    # estimates. We can also set these fairly modest gains that will be a
    # bit sloppy but shouldn’t shake your rig apart if it’s built poorly.
    # Make sure to tune the gains up when you have everything else working
    # to a stiffness that is applicable to your application.
    ENCODER_BANDWIDTH = 100 # 100 default, 1000 for high power
    # Tolerance for encoder offset float
    # Since hall sensors are low resolution feedback, we also bump up the
    # offset calibration displacement to get better calibration accuracy.
    ENCODER_OFFSET_FLOAT_TOLERANCE = 0.05 # relaxed accuracy, we have pulse every 0.02 turns
    # Since the hall feedback only has 42 counts per revolution, we want to
    # reduce the velocity tracking bandwidth to get smoother velocity
    # estimates. We can also set these fairly modest gains that will be a
    # bit sloppy but shouldn’t shake your rig apart if it’s built poorly.
    # Make sure to tune the gains up when you have everything else working
    # to a stiffness that is applicable to your application.
    #
    # The hall feedback has 6 states for every pole pair in the motor. Since
    # we have 7 pole pairs, we set the cpr to 7*6 = 42.
    # CPR will be computed as pole_pairs * 6
    # HALL sensors are at gpio 9,10,11 and 12,13,14
    # Scan Distance is pole pairs * 2 * pi is one turn
    CALIB_SCAN_DISTANCE = 90 # 50 default, 90 for hoverboard
    CALIB_RANGE = 0.5 # 0.1 default, 0.5 for hoverboard, The error threshold for encoder offset calibration, in turns.
    
    
    # PID Controller
    # ==============
    # Velocity limit in turns/s
    # 75% * bus voltage * motor kv in RPM, converted to counts/s
    # 80% of the encoder’s max speed
    # Not higher than 35000 electrical RPM
    # Max Speed 60km/h = 1000m/min = 16.67m/s 
    # Wheel diameter 0.147m => circumference is 0.147m * 3.141 = 0.462m
    # 16.67m/s / 0.462m = 36 rev/s
    VEL_LIMIT = 40 # 40 regular, for calibration use 5
    POS_GAIN = 200. # 20 default, for anticogging calibration the gain should be large like 200.0
    VEL_GAIN = 0.02 # 0.02 default, 0.02 for hoverboard
    VEL_INTEGRATOR_GAIN = 0.1 # 0.1 default, 0.1 for hoverboard
    CONTROL_MODE = CONTROL_MODE_VELOCITY_CONTROL
    
    # Temperature
    # ===========
    TEMP_PIN = 0 # GPIO 1,2,3,4,5 can be analog in, 0 is off
    R_LOAD = 10000 # 10kOhm
    R_NOMINAL = 10000 # 10kOhm
    R_BETA = 3380 # 3380 for 10kOhm
    T_MIN = -20 # -20 default
    T_MAX = 150 # 100 default
    
    def __init__(self, axis_num, erase_config):
        """
        Initializes MotorConfig class by finding odrive, erase its
        configuration, and grabbing specified axis object.

        :param axis_num: Which channel/motor on the odrive your referring to.
        :type axis_num: int (0 or 1)
        :param erase_config: Erase existing config before setting new config.
        :type erase_config: bool (True or False)
        """

        self.axis_num = axis_num

        self.erase_config = erase_config

        # Connect to Odrive
        print("Looking for ODrive...")
        self._find_odrive()
        print("Found ODrive.")

    def _find_odrive(self):
        # connect to Odrive
        self.odrv = odrive.find_any()
        self.odrv_axis = getattr(self.odrv, "axis{}".format(self.axis_num))

    def configure(self):
        """
        Configures the odrive device for motor.
        """

        if self.erase_config:
            # Erase pre-existing configuration
            print("Erasing pre-exsisting configuration...")
            try:
                self.odrv.erase_configuration()
            except Exception:
                pass

        self._find_odrive()

        # Brake Resistor and Regenerative Braking
        # Set this to True if using a brake resistor
        self.odrv.config.enable_brake_resistor                      = True
        self.odrv.config.brake_resistance                           = self.R_BREAK
        self.odrv.config.dc_max_negative_current                    = self.MAX_REGEN_CURRENT
        
        # Motor
        self.odrv_axis.motor.config.motor_type                      = self.MOTOR_TYPE
        self.odrv_axis.motor.config.pole_pairs                      = self.MOTOR_POLE_PAIRS
        self.odrv_axis.motor.config.current_lim                     = self.MOTOR_CURRENT_LIMIT
        self.odrv_axis.motor.config.current_lim_margin              = self.CURRENT_LIMIT_MARGIN
        self.odrv_axis.motor.config.calibration_current             = self.CALIBRATION_CURRENT
        self.odrv_axis.motor.config.requested_current_range         = self.CURRENT_RANGE
        self.odrv_axis.motor.config.resistance_calib_max_voltage    = self.RESISTANCE_CALIBRATION_MAX_VOLTAGE
        self.odrv_axis.motor.config.current_control_bandwidth       = self.CURRENT_CONTROL_BANDWIDTH
        self.odrv_axis.motor.config.torque_constant                 = 8.27 / self.MOTOR_KV

        # Encoder
        self.odrv_axis.encoder.config.mode                          = self.ENCODER_MODE
        self.odrv_axis.encoder.config.cpr                           = self.MOTOR_POLE_PAIRS * 6.0        
        self.odrv_axis.encoder.config.calib_scan_distance           = self.CALIB_SCAN_DISTANCE
        self.odrv_axis.encoder.config.bandwidth                     = self.ENCODER_BANDWIDTH
        self.odrv_axis.controller.config.pos_gain                   = self.POS_GAIN
        self.odrv_axis.controller.config.vel_gain                   = (
                    self.VEL_GAIN
                    * self.odrv_axis.motor.config.torque_constant
                    * self.odrv_axis.encoder.config.cpr
        )
        self.odrv_axis.controller.config.vel_integrator_gain        = (
                    self.VEL_INTEGRATOR_GAIN
                    * self.odrv_axis.motor.config.torque_constant
                    * self.odrv_axis.encoder.config.cpr
        )
        self.odrv_axis.controller.config.vel_limit                  = self.VEL_LIMIT

        # Motor Temperature Sensor Setup
        if self.TEMP_PIN > 0:
            if self.TEMP_PIN == 1:
                self.odrv.config.gpio1_mode                         = GPIO_MODE_ANALOG_IN
            elif self.TEMP_PIN == 2:
                self.odrv.config.gpio2_mode                         = GPIO_MODE_ANALOG_IN
            elif self.TEMP_PIN == 3:
                self.odrv.config.gpio3_mode                         = GPIO_MODE_ANALOG_IN
            elif self.TEMP_PIN == 4:
                self.odrv.config.gpio4_mode                         = GPIO_MODE_ANALOG_IN
            elif self.TEMP_PIN == 5:
                self.odrv.config.gpio5_mode                         = GPIO_MODE_ANALOG_IN

            set_motor_thermistor_coeffs(self.odrv_axis, self.R_LOAD, self.R_NOMINAL, self.R_BETA, self.T_MIN, self.T_MAX)
            self.odrv_axis.motor.motor_thermistor.config.gpio_pin   = self.TEMP_PIN
            self.odrv_axis.motor.motor_thermistor.config.enabled    = True
            self.odrv.get_adc_voltage(self.TEMP_PIN)
        else:
            self.odrv_axis.motor.motor_thermistor.config.enabled    = False

        # Set in position control mode so we can control the position of the wheel
        self.odrv_axis.controller.config.control_mode               = self.CONTROL_MODE

        # In the next step we are going to start powering the motor and so we
        # want to make sure that some of the above settings that require a
        # reboot are applied first.

        # Motors must be in IDLE mode before saving
        self.odrv_axis.requested_state  = AXIS_STATE_IDLE
        try:
            print("Saving manual configuration and rebooting...")
            is_saved = self.odrv.save_configuration()
            if not is_saved:
                print("Error: Configuration not saved. Are all motors in IDLE state?")
            else:
                print("Calibration configuration saved.")

            print("Manual configuration saved.")
        except Exception as e:
            pass

        self._find_odrive()

        #######################################################################################
        # CONDUCT THE CALIBRATION
        # Things are going to happen here that will make the motor move. Make sure that the
        # motor is free to move and that you are ready to unplug the power if something goes
        # wrong.
        #######################################################################################

        input("Make sure the motor is free to move, then press enter...")

        print("Calibrating Odrive motor (you should hear a " "beep)...")

        self.odrv_axis.requested_state = AXIS_STATE_MOTOR_CALIBRATION 

        # Wait for calibration to take place
        time.sleep(10)

        if self.odrv_axis.motor.error != 0:
            print(
                "Error: Odrive reported an error of {} while in the state "
                "AXIS_STATE_MOTOR_CALIBRATION.".format(self.odrv_axis.motor.error)
            ) 
            dump_errors(self.odrv, clear=True)
            print(                
                "Printing out Odrive motor data for "
                "debug:\n{}".format(self.odrv_axis.motor.error, self.odrv_axis.motor)
            )

            sys.exit(1)

        if (
            self.odrv_axis.motor.config.phase_inductance <= self.MIN_PHASE_INDUCTANCE
            or self.odrv_axis.motor.config.phase_inductance >= self.MAX_PHASE_INDUCTANCE
        ):
            print(
                "Error: After odrive motor calibration, the phase inductance "
                "is at {}, which is outside of the expected range. Either widen the "
                "boundaries of MIN_PHASE_INDUCTANCE and MAX_PHASE_INDUCTANCE (which "
                "is between {} and {} respectively) or debug/fix your setup. Printing "
                "out Odrive motor data for debug:\n{}".format(
                    self.odrv_axis.motor.config.phase_inductance,
                    self.MIN_PHASE_INDUCTANCE,
                    self.MAX_PHASE_INDUCTANCE,
                    self.odrv_axis.motor,
                )
            )

            sys.exit(1)

        if (
            self.odrv_axis.motor.config.phase_resistance <= self.MIN_PHASE_RESISTANCE
            or self.odrv_axis.motor.config.phase_resistance >= self.MAX_PHASE_RESISTANCE
        ):
            print(
                "Error: After odrive motor calibration, the phase resistance "
                "is at {}, which is outside of the expected range. Either raise the "
                "MAX_PHASE_RESISTANCE (which is between {} and {} respectively) or "
                "debug/fix your setup. Printing out Odrive motor data for "
                "debug:\n{}".format(
                    self.odrv_axis.motor.config.phase_resistance,
                    self.MIN_PHASE_RESISTANCE,
                    self.MAX_PHASE_RESISTANCE,
                    self.odrv_axis.motor,
                )
            )

            sys.exit(1)

        # If all looks good, then lets tell ODrive that saving this calibration
        # to persistent memory is OK
        self.odrv_axis.motor.config.pre_calibrated = True

        # Motors must be in IDLE mode before saving
        self.odrv_axis.requested_state  = AXIS_STATE_IDLE
        try:
            print("Saving manual configuration and rebooting...")
            is_saved = self.odrv.save_configuration()
            if not is_saved:
                print("Error: Configuration not saved. Are all motors in IDLE state?")
            else:
                print("Calibration configuration saved.")

            print("Manual configuration saved.")
        except Exception as e:
            pass

        self._find_odrive()

        # Check the alignment between the motor and the hall sensor. Because of
        # this step you are allowed to plug the motor phases in random order and
        # also the hall signals can be random. Just don’t change it after
        # calibration.
        print("Calibrating Odrive for hall encoder...")
        self.odrv_axis.requested_state = AXIS_STATE_ENCODER_HALL_POLARITY_CALIBRATION

        # Wait for calibration to take place
        time.sleep(10)

        if self.odrv_axis.motor.error != 0:
            print(
                "Error: Odrive reported an error of {} while in the state "
                "AXIS_STATE_ENCODER_HALL_POLARITY_CALIBRATION.".format(self.odrv_axis.motor.error)
            ) 
            dump_errors(self.odrv, clear=True)
            print(                
                "Printing out Odrive motor data for "
                "debug:\n{}".format(self.odrv_axis.motor.error, self.odrv_axis.motor)
            )

            sys.exit(1)

        print("Calibrating Odrive for encoder offset...")
        self.odrv_axis.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION

        # Wait for calibration to take place
        time.sleep(10)

        if self.odrv_axis.motor.error != 0:
            print(
                "Error: Odrive reported an error of {} while in the state "
                "AXIS_STATE_ENCODER_OFFSET_CALIBRATION.".format(self.odrv_axis.motor.error)
            ) 
            dump_errors(self.odrv, clear=True)
            print(                
                "Printing out Odrive motor data for "
                "debug:\n{}".format(self.odrv_axis.motor.error, self.odrv_axis.motor)
            )

            sys.exit(1)

        # If all looks good, then lets tell ODrive that saving this calibration
        # to persistent memory is OK
        self.odrv_axis.encoder.config.pre_calibrated = True

        print("Calibrating Odrive for anticogging. This can take 5-30mins. Be patient.")
        self.odrv_axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

        self.odrv_axis.controller.start_anticogging_calibration()

        print("Still calibrating anticogging: ", end="", flush = True)
        i = 0
        while self.odrv_axis.controller.config.anticogging.calib_anticogging:
            time.sleep(15)
            i = i + 1
            print("Still calibrating anticogging: {:>4.2f} mins".format(i*15./60.), end="\r", flush = True)

        if self.odrv_axis.motor.error != 0:
            print(
                "Error: Odrive reported an error of {} while performing "
                "start_anticogging_calibration().".format(self.odrv_axis.motor.error)
            ) 
            dump_errors(self.odrv, clear=True)
            print(                
                "Printing out Odrive motor data for "
                "debug:\n{}".format(self.odrv_axis.motor.error, self.odrv_axis.motor)
            )

            sys.exit(1)

        # If all looks good, then lets tell ODrive that saving this calibration
        # to persistent memory is OK
        self.odrv_axis.controller.config.anticogging.pre_calibrated = True

        # Motors must be in IDLE mode before saving
        self.odrv_axis.requested_state = AXIS_STATE_IDLE
        try:
            print("Saving calibration configuration and rebooting...")
            is_saved = self.odrv.save_configuration()
            if not is_saved:
                print("Error: Configuration not saved. Are all motors in IDLE state?")
            else:
                print("Calibration configuration saved.")
        except Exception as e:
            pass

        self._find_odrive()

        print("Odrive configuration finished.")

    def mode_idle(self):
        """
        Puts the motor in idle (i.e. can move freely).
        """

        self.odrv_axis.requested_state = AXIS_STATE_IDLE

    def mode_close_loop_control(self):
        """
        Puts the motor in closed loop control.
        """

        self.odrv_axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

    def move_input_pos(self, angle):
        """
        Puts the motor at a certain angle.

        :param angle: Angle you want the motor to move.
        :type angle: int or float
        """

        self.odrv_axis.controller.input_pos = angle / 360.0


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Motor Calibration")

    # Argument for axis_num
    parser.add_argument(
        "-a",
        "--axis_num",
        metavar="<axis_num>",
        dest="axis_num",
        type=int,
        choices=[0, 1],  # Only allow 0 or 1
        help="Motor axis number which can only be 0 or 1.",
        default = 1
    )

    # Argument for erase_config
    parser.add_argument(
        "-e",
        "--erase_config",
        action="store_true",  # If present, set to True. If absent, set to False.
        help="Flag to determine if the config should be erased.",
        default = False
    )

    # Argument to conduct motor test (make sure motor can move freely)
    parser.add_argument(
        "--motor_test",
        action="store_true",  # If present, set to True. If absent, set to False.
        help="Flag to determine if the config should be erased.",
        default = False
    )

    args = parser.parse_args()

    motor_config = MotorConfig(
        axis_num=args.axis_num, erase_config=args.erase_config
    )
    motor_config.configure()

    if args.motor_test:
        print("Placing motor in close loop. If you move motor, motor will resist you.")
        motor_config.mode_close_loop_control()

        print("CONDUCTING MOTOR TEST")

        # Go from 0 to 360 degrees in increments of 30 degrees
        for angle in range(0, 390, 30):
            print("Setting motor to {} degrees.".format(angle))
            motor_config.move_input_pos(angle)
            time.sleep(5)

        print("Placing motor in idle. If you move motor, motor will move freely")
        motor_config.mode_idle()
