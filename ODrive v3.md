# Setting up ODrive V3

## Software

Install and test odrive tool software

```
pip install --upgrade odrive
odrivetool
odrv0.vbus_voltage
exit()
```

Update firmware
```
odrivetool dfu
``````

## Setup Motor
Order of the three plugs is not relevant. You can swap two wires for motor direction to go backwards.


### Start Fresh
```
odrv0.erase_configuration()
```

### General
```
odrv0.config.enable_brake_resistor = True
odrv0.config.brake_resistance = 2
odrv0.config.dc_max_negative_current = -36                    
```

### M0
```
odrv0.axis0.motor.config.current_lim = 20                     # 10Amp for safety, 60A default, max Motor Wattage / Battery Nominal
odrv0.axis0.controller.config.vel_limit = 2                  # turns per second
# [depends on battery]
odrv0.axis0.motor.config.pole_pairs = 7                       # pole pairs devided by 2
odrv0.axis0.motor.config.torque_constant = 8.27 / 192         # [192kV]
odrv0.axis0.motor.config.motor_type = MOTOR_TYPE_HIGH_CURRENT # 0
```

### M1
```
odrv0.axis1.motor.config.current_lim = 20
odrv0.axis1.controller.config.vel_limit = 2
odrv0.axis0.motor.config.pole_pairs = 7
odrv0.axis0.motor.config.torque_constant = 8.27 / 192
odrv0.axis0.motor.config.motor_type = MOTOR_TYPE_HIGH_CURRENT
```

## Calibrate Motor 

It says to start with 10 and once you have tuned ODrive you can increase to 60A.
For  more than 60A I need to increase the requested current range first, then save and reboot. See towards end

### Calibration Settings

### M0
```
odrv0.axis0.motor.config.current_lim_margin = 16
odrv0.axis0.motor.config.calibration_current = 10            # default 10A, larger for larger motor
odrv0.axis0.motor.config.requested_current_range = 60        # > current_lim + curren_lim_margin, but as low as possible
# resistance_calib_max_voltage < 0.5 vbus_voltage
# resistance_calib_max_voltage = calibration_current (10) * phase_resistance (0.04)
odrv0.axis0.motor.config.resistance_calib_max_voltage = 5    # max votlage used to measure motor resitance
odrv0.axis0.motor.config.current_control_bandwidth = 100     # 1000 default, lower for hub motor
odrv0.axis0.controller.config.vel_limit = 5                  # turns per second
```

### M1
```
odrv0.axis1.motor.config.current_lim_margin = 16
odrv0.axis1.motor.config.calibration_current = 10
odrv0.axis1.motor.config.requested_current_range = 60
odrv0.axis1.motor.config.resistance_calib_max_voltage = 5
odrv0.axis1.motor.config.current_control_bandwidth = 100
odrv0.axis1.controller.config.vel_limit = 5
```

### Calibrate Motor
```
odrv0.axis0.requested_state = AXIS_STATE_MOTOR_CALIBRATION
odrv0.axis1.requested_state = AXIS_STATE_MOTOR_CALIBRATION
```

### Errors
```
dump_errors(odrv0)
odrv0.clear_errors()
```
### Example Results
```
odrv0.axis0.motor.error                   # 0
odrv0.axis0.motor.config.phase_inductance # 0.00033594953129068017 (float)
odrv0.axis0.motor.config.phase_resistance # 0.1793474406003952 (float)

odrv0.axis1.motor.error                   # 0
odrv0.axis1.motor.config.phase_inductance # 0.00033594953129068017 (float)
odrv0.axis1.motor.config.phase_resistance # 0.1793474406003952 (float)
```

### If no Errors
```
odrv0.axis0.motor.config.pre_calibrated = True # phase resitance and phase inductance are valid
odrv0.axis1.motor.config.pre_calibrated = True # phase resitance and phase inductance are valid
```

### Save

```
odrv0.save_configuration()
```


## Sensors

### Configure Sensor Connector on Turnigy 192KV Motor

```
- Red V++
- Blu Temp
- Grn Hall1 - ODrive Hall A
- Wht Hall2 - ODrive Hall B
- Brw Hall3 - ODrive Hall Z
- Blk GND
```

```
GND   - V+      : 10MOhm
GND   - Temp    : 9.52KOhm @ RT
Temp  - V+      : 10MOhm
Hall1 - GND/Vcc : Inf
Hall2 - GND/Vcc : Inf
Hall3 - GND/Vcc : Inf
```

On ODrive Hall1,2,3 3.3kOhm pull up to VCC 3.3V

**Hall Effect** current flows through strip, magnetic field pernedicular to strop deflect current through strip to one side so that there is voltage difference from one to the other side of the strip. This is amplified to produce output voltage.
Therefor Hall sensor has positiv & negative powers supply input and signal output. 


| **M0** |     |              |
| --     | --  | --           | 
| Pin  1 | VCC | 3.3V  M0     | 
| Pin  2 |     | Not Connected| 
| Pin  3 | A   | Hall 1 M0    | 
| Pin  4 | B   | Hall 2 M0    | 
| Pin  5 | Z   | Hall 3 M0    | 
| Pin  6 | GND | GND M0       | 

| **M1** |     |              |
| --     | --  | --           | 
| Pin  7 | VCC | 3.3V M1      | 
| Pin  8 |     | Not Connected|  
| Pin  9 | A   | Hall 1 M1    | 
| Pin 10 | B   | Hall 2 M1    | 
| Pin 11 | Z   | Hall 3 M1    | 
| Pin 12 | GND | GND M1       | 

**Need to add 22nF bypass capacitors between Hall pin and GND.**

### Setup Hall Sensors

#### M0
```
odrv0.axis0.encoder.config.mode = ENCODER_MODE_HALL
odrv0.axis0.encoder.config.cpr = 7 * 6 # 7 poles pairs 6 states for HALL sensor
odrv0.config.gpio9_mode = GPIO_MODE_DIGITAL
odrv0.config.gpio10_mode = GPIO_MODE_DIGITAL
odrv0.config.gpio11_mode = GPIO_MODE_DIGITAL
```

#### M1
```
odrv0.axis1.encoder.config.mode = ENCODER_MODE_HALL
odrv0.axis1.encoder.config.cpr = 7 * 6 # 7 poles pairs 6 states for HALL sensor
odrv0.config.gpio12_mode = GPIO_MODE_DIGITAL
odrv0.config.gpio13_mode = GPIO_MODE_DIGITAL
odrv0.config.gpio14_mode = GPIO_MODE_DIGITAL
```

#### Sensor Calibration Settings

```
odrv0.axis0.encoder.config.calib_scan_distance = 45          # pole pairs * 2 * pi
odrv0.axis0.encoder.config.calib_range = 0.05                # error offset for encoder calibration in turns [relaxed accuracy, we have pulse every 0.02 turns]

odrv0.axis1.encoder.config.calib_scan_distance = 45
odrv0.axis1.encoder.config.calib_range = 0.05
```

#### Save

```
odrv0.save_configuration()
```

### Calibrate Sensors

M0
```
# Polarity
odrv0.axis0.requested_state = AXIS_STATE_ENCODER_HALL_POLARITY_CALIBRATION 
# Offset
odrv0.axis0.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
# Phase
odrv0.axis0.requested_state = AXIS_STATE_ENCODER_HALL_PHASE_CALIBRATION
# Index
odrv0.axis0.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH
```

M1
```
odrv0.axis1.requested_state = AXIS_STATE_ENCODER_HALL_POLARITY_CALIBRATION 
odrv0.axis1.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
odrv0.axis1.requested_state = AXIS_STATE_ENCODER_HALL_PHASE_CALIBRATION
odrv0.axis1.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH
```

```
dump_errors(odrv0)
odrv0.clear_errors()
```

```
odrv0.axis0.encoder
odrv0.axis1.encoder
```
phase_offset_float should be close to -1.5, -0.5, 0.5, or 1.5, 


### If no ERRORS Set Calibrated
```
odrv0.axis0.encoder.config.pre_calibrated = True
odrv0.axis1.encoder.config.pre_calibrated = True
```

### Save

```
odrv0.save_configuration()
```

## Position and Velocity Control

M0
```
odrv0.axis0.controller.config.pos_gain = 1 # default 20
odrv0.axis0.controller.config.vel_gain = 0.02 * odrv0.axis0.motor.config.torque_constant * odrv0.axis0.encoder.config.cpr # [0.036]
odrv0.axis0.controller.config.vel_integrator_gain = 0.1 * odrv0.axis0.motor.config.torque_constant * odrv0.axis0.encoder.config.cpr # [0.18]
odrv0.axis0.controller.config.vel_limit = 130 #
odrv0.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
```

M1
```
odrv0.axis1.controller.config.pos_gain = 1 # default 20
odrv0.axis1.controller.config.vel_gain = 0.02 * odrv0.axis1.motor.config.torque_constant * odrv0.axis1.encoder.config.cpr # [0.036]
odrv0.axis1.controller.config.vel_integrator_gain = 0.1 * odrv0.axis1.motor.config.torque_constant * odrv0.axis1.encoder.config.cpr # [0.32]
odrv0.axis1.controller.config.vel_limit = 130 #
odrv0.axis1.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
```

### If ALL good
```
odrv0.axis0.config.startup_closed_loop_control = True
odrv0.axis1.config.startup_closed_loop_control = True
odrv0.save_configuration()
```

## Read data
```
odrv0.axis0.motor

odrv0.axis1.motor
```

## Test Motor Constant Velocity Mode
```
# Start Spinning
odrv0.axis0.controller.input_vel = 1.5
# Stop Spinning
odrv0.axis0.controller.input_vel = 0
odrv0.axis0.requested_state = AXIS_STATE_IDLE
```

## Set Current to MAX
```
odrv0.axis0.motor.config.requested_current_range = 90 # [Absolute Maximum Amp for motor]
odrv0.axis0.controller.config.vel_limit = 130 # [turns/sec]

odrv0.axis1.motor.config.requested_current_range = 90 # [Absolute Maximum Amp for motor]
odrv0.axis1.controller.config.vel_limit = 130 # [turns/sec]

odrv0.save_configuration()
```


### Test Hal Sensor
```
odrv0.axis0.encoder.shadow_count # and look at your value. Then turn your motor by hand and see if that value changes.
odrv0.axis0.encoder.config.cpr   # must reflect th counts after one full turn
```

## Setup Thermistors
On PCB
```
AVCC - 10kThermistor - 3.3k - AGND
2.2uF Cap over 3.3k
```

Analog input for ODrive 0..3.3V

```
AVCC (Pin 6)
AGND (Pin 7)
Therm 1 GPIO1 (Pin 11)
Therm 2 GPIO2 (Pin 12)
```

```
set_motor_thermistor_coeffs(odrv0.axis0,3300, 10000, 3950, 100, 120)
set_motor_thermistor_coeffs(odrv0.axis1,3300, 10000, 3950, 100, 120)
odrv0.config.gpio1_mode = GPIO_MODE_ANALOG_IN
odrv0.config.gpio2_mode = GPIO_MODE_ANALOG_IN
odrv0.config.gpio3_mode = GPIO_MODE_ANALOG_IN
odrv0.config.gpio4_mode = GPIO_MODE_ANALOG_IN
odrv0.axis0.motor.motor_thermistor.config.gpio_pin = 1
odrv0.axis1.motor.motor_thermistor.config.gpio_pin = 2
odrv0.axis0.motor.motor_thermistor.config.enabled = True
odrv0.axis1.motor.motor_thermistor.config.enabled = True
odrv0.get_adc_voltage(1)
odrv0.get_adc_voltage(2)
odrv0.get_adc_voltage(3)
odrv0.get_adc_voltage(4)
```

