#!/usr/bin/env python3
#####################################################################
# Read Gamepad Events with evdev.
# Consider Connect and Disconnect with udev.
# Control Left and Right Speed of a vehicle with two forward/backward motors.
# Urs Utzinger
# 2023
#####################################################################
# Description:
# Joystick up increases speed, down decreases speed
# Joystick left increases speed on right motor and decreases speed of left motor
# Button top: brings system to halt (any joystick moved will reduce speed)
# Button bottom: steers to center, both motors same speed
# Button C: Turbo mode, increase gains
# Button D: Battery display, Speed display, OFF
#
# Can adjust joystick sensitivity and speed increase/decrease
# Can decreasing speed faster than increasing speed
# Should work forwards and backwards
#
# Motor control is not implemented but speed set values are displayed
#####################################################################

DISPLAY = True # Display speed as bar graph
deviceName_1="Umido ESoul DH2 Mouse"
deviceName_2="Umido ESoul DH2 Keyboard"

# Notes
#####################################################################

# UDEV Event masks are
######################
# POLLIN    1 data available to read
# POLLPRI   2 urgent data to read
# POLLOUT   4 ready for output
# POLLERR   8 error conditions of some sort
# POLLHUP   16 hung up
# POLLNVAL  32 invalid request
# POLLRDHUP 8192 peer closed connected 
# e.g. pollerObject.register(monitor, select.POLLIN+self.POLLOUT)
#####################################################################

# Keys Umido ESoul DH2
######################
# - Joystick
# REL_X         -6(left) ... +7(right)
# REL_Y         -6(up)   ... +7(down)
# - Large front button also button A
# BTN_LEFT       pushed value 1, released 0
# - Second front button also button B
# KEY_ESC        pushed value 1, continuous 2, released 0
# - Button C
# KEY_VOLUMEUP   pushed value 1, continuous 2, released 0
# - Button D
# KEY_VOLUMEDOWN pushed value 1, continuous 2, released 0
#####################################################################
# Example input events for joystick, keys and buttons
#
# Each joystick move gives both X and Y event
# Type: EV_REL, Code: REL_X, Value: 2
# Type: EV_REL, Code: REL_Y, Value: 1
# Type: EV_SYN, Code: SYN_REPORT, Value: 0
#
# KEY value can be 1 for pushed, 2 for continuously pushed, 0 for released
# Type: EV_MSC, Code: MSC_SCAN, Value: 786665
# Type: EV_KEY, Code: KEY_VOLUMEUP, Value: 1
# Type: EV_SYN, Code: SYN_REPORT, Value: 0
#
# Type: EV_MSC, Code: MSC_SCAN, Value: 589825
# Type: EV_KEY, Code: ['BTN_LEFT', 'BTN_MOUSE'], Value: 1
# Type: EV_SYN, Code: SYN_REPORT, Value: 0
#####################################################

# Tank Drive
###########
# speed: base speed
# left_right:  left versus right -1..+1
# speed_Left:  set speed for left motor
# speed_Right: set speed for right motor
# if left_right is 0 speed_left is same as speed_right.
# if left_right is -1 speed_left is zero
#####################################################

# Imports
import functools
import pyudev
import select
import time
import logging
from evdev import InputDevice, ecodes

#####################################################
# Function Declarations
#####################################################

def clamp(val, smallest, largest): 
    '''
    Clip val to [smallest, largest]
    '''
    if val < smallest: return smallest
    if val > largest: return largest
    return val

def handleEvent(event=None, tank=None, logger=None):
    '''
    Decode the gamepad events and call corresponding drive routines
    '''
    if event is not None:

        if event.type == ecodes.EV_REL:
            if event.code == ecodes.ecodes['REL_X']:
                if tank is not None:
                    # steer left or right
                    if logger is not None:
                        logger.log(logging.INFO, "Type: {}, Code: {}, Value: {}".format(ecodes.EV[event.type], ecodes.bytype[event.type][event.code], event.value))
                    tank.update(REL_X=event.value)
            elif event.code == ecodes.ecodes['REL_Y']:
                if tank is not None:
                    # go faster or slower
                    if logger is not None:
                        logger.log(logging.INFO, "Type: {}, Code: {}, Value: {}".format(ecodes.EV[event.type], ecodes.bytype[event.type][event.code], event.value))
                    tank.update(REL_Y=event.value)
        elif event.type == ecodes.EV_KEY:
            if event.code == ecodes.ecodes['KEY_ESC']:
                if tank is not None:
                    if logger is not None:
                        logger.log(logging.INFO, "Type: {}, Code: {}, Value: {}".format(ecodes.EV[event.type], ecodes.bytype[event.type][event.code], event.value))
                    if event.value==1:
                        tank.center()
            elif event.code == ecodes.ecodes['KEY_VOLUMEUP']:
                # Show battery
                if logger is not None:
                    logger.log(logging.INFO, "Type: {}, Code: {}, Value: {}".format(ecodes.EV[event.type], ecodes.bytype[event.type][event.code], event.value))
                if tank is not None:
                    if event.value==1:
                        tank.turbo()
            elif event.code == ecodes.ecodes['KEY_VOLUMEDOWN']:
                # Show lights/speed
                # Show battery
                if logger is not None:
                    logger.log(logging.INFO, "Type: {}, Code: {}, Value: {}".format(ecodes.EV[event.type], ecodes.bytype[event.type][event.code], event.value))
                if tank is not None:
                    if event.value==1:
                        pass # not implemented
            elif event.code == ecodes.ecodes['BTN_LEFT']:
                if logger is not None:
                    logger.log(logging.INFO, "Type: {}, Code: {}, Value: {}".format(ecodes.EV[event.type], ecodes.bytype[event.type][event.code], event.value))
                if tank is not None:
                    if event.value == 1:
                        tank.stop() # toggle stopping mode
        else:
            pass

#####################################################
# Classes
#####################################################

class BTDevice(object):
    '''
    Keep track of bluetooth device
    '''
    def __init__(self, name="", path="", device=None, poller=None, timeout=5):
        self.name    = name
        self.path    = path
        self.device  = device
        self.poller  = poller    
        self.timeout = timeout  # poller timeout in milliseconds

class TankDrive(object):
    '''
    Tank Drive
    speed:       speed base 
    left_right:  left versus right -1..+1
    speed_Left:  set speed for left motor
    speed_Right: set speed for right motor
    '''
    
    def __init__(self):
        self.MAXUPDOWN     =   7    # max joystick value in Y direction, needs to be positive
        self.MINUPDOWN     =  -6    # min joystick value, needs to be negative
        self.MAXLR         =   7    # max joystick value in X direction
        self.MINLR         =  -6    # min joystick value
        self.SENS          =   1.5  # non linear joystick sensitivity, small changes remain small, large changes become larger
        self.BREAK         =   2    # change speed faster when slowing down
        self.MAX_SPEED     =  30    # max speed value
        self.MIN_SPEED     = -30    # min speed value
        self.THRESH_SPEED  =   0.1  # for stopping down, speed below this value amounts to zero
        self.MAX_RATIO     =   1.   # left versus right
        self.MIN_RATIO     =  -1.   # left versus right
        self.THRESH_RATIO  =   0.1  # for stopping down, ratio below this value amounts to zero
        self.SPEED_GAIN    =  -0.1  # how fast to increase/decrease speed, flip direction (negative)
        self.RATIO_GAIN    =   0.01 # how fast to steer
        self.TURBO_GAIN    =   2.0  # increase gains with this when turbo is pressed
        self.speed         =   0.   # initialize speed to zero
        self.ratio         =   0.   # initialize steering to straight
        self.speed_left    =   0.   # initialize left & right zero
        self.speed_right   =   0.
        self.eco           =  True  # use smaller gains
        self.stopping      =  False # not ins stopping mode, speed can only increase and steering straighten
        self.locked        =  False # system not locked to zero
        self.ratio_previous=   0.   # keep track of last steering value
        self.speed_previous=   0.   # keep track of last speed value

    def update(self, REL_X=0, REL_Y=0):
        '''
        Update motor speeds based on joystick input
        '''
        ##############################################################################################
        # Joystick conversion
        # Will create values between -1 and 1
        # non linear adjustments
        
        # REL_Y negative is up and pos down
        # We invert value to make acceleration positive and braking negative by using negative gain;-)

        # Sometimes we are getting erroneous values of -123 in Y or X, therefore reject value if out of bounds

        if (REL_Y>=self.MINUPDOWN and REL_Y<=self.MAXUPDOWN and REL_X>=self.MINLR and REL_X<=self.MAXLR):
            if REL_Y < 0: _up_down    = - (REL_Y/self.MINUPDOWN)**self.SENS # -1..1
            else:         _up_down    =   (REL_Y/self.MAXUPDOWN)**self.SENS # -1..1
            if REL_X < 0: _left_right = - (REL_X/self.MINLR)**self.SENS     # -1..1
            else:         _left_right =   (REL_X/self.MAXLR)**self.SENS     # -1..1

            _speed_inc = self.SPEED_GAIN * _up_down
            if self.speed > 0:         # FORWARD MODE
                if _speed_inc < 0:     # SLOWING DOWN
                    _speed_inc = _speed_inc * self.BREAK # slow down more than accelerate
                else:                  # ACCELERATING 
                    if self.stopping:  #  if we actually want to slow down (front button was pressed) reverse the increase to a decrease
                        _speed_inc = - _speed_inc
                
            else:                      # BACKWARD MODE
                if _speed_inc > 0:     # SLOWING DOWN
                    _speed_inc = _speed_inc * self.BREAK # slow down more than accelerate
                else:                  # ACCELERATING
                    if self.stopping:  #  if we want to slow down reverse the increase to a decrease
                        _speed_inc = - _speed_inc

            # Standard driving
            if not self.locked:
                self.speed_previous = self.speed # keep previous speed
                self.speed += _speed_inc   # update speed
                self.speed = clamp(self.speed, self.MIN_SPEED, self.MAX_SPEED) # clamp speed

            # If slowing down to zero and speed close to zero, lock onto zero
            if self.stopping: # lock onto 0
                if abs(self.speed) < self.THRESH_SPEED : 
                    self.speed = 0.
                    self.locked = True

            # Steering
            # Left-Right ratio
            _ratio_inc = (self.RATIO_GAIN * _left_right) 

            if self.ratio >= 0:        # LEFT MODE
                if _ratio_inc > 0:     # STEER
                    if self.stopping:  # want to straighten
                        _ratio_inc = - _ratio_inc
            else:                      # RIGHT MODE
                if _ratio_inc < 0:     # STEER
                    if self.stopping:  # want to straighten
                        _ratio_inc = - _ratio_inc

            self.ratio_previous =  self.ratio # keep previous
            self.ratio  += _ratio_inc  # update
            self.ratio = clamp(self.ratio, self.MIN_RATIO, self.MAX_RATIO) # clamp steering

            if self.stopping:  # lock onto 0
                if abs(self.ratio) < self.THRESH_RATIO: 
                    self.ratio = 0.

            # Left versus right motor
            # if ratio is -1 left motor is 0 and right motor is 2 * speed
            # average left and right speed is speed
            self.speed_left  = self.speed + self.speed *self.ratio
            self.speed_right = self.speed - self.speed *self.ratio

    def turbo(self):
        '''
        Speedup with higher or lower gains
        '''
        if self.eco:
            self.eco=False
            self.SPEED_GAIN = self.SPEED_GAIN * self.TURBO_GAIN
        else:
            self.eco=True
            self.SPEED_GAIN = self.SPEED_GAIN / self.TURBO_GAIN

    def center(self):
        '''
        Both motors same speed
        '''
        self.ratio = 0.
        self.speed_left  = self.speed + self.speed *self.ratio
        self.speed_right = self.speed - self.speed *self.ratio

    def stop(self):
        '''
        Want to slow down and straighten
        Any joystick input will decrease the speed and straighten the vehicle
        '''
        if self.stopping == True:
            self.stopping = False # disable stopping mode
            self.locked = False   # disengage lock
        else:
            self.stopping = True  # enable stopping mode

###########################################################################################
###########################################################################################

if __name__ == "__main__":

    #####################################################################
    # Setup
    #####################################################################

    # Input devices to be watched
    # Keypad and Joystick
    input_pollInterval = 0.01 # how long to wait for next poll
    joystick = BTDevice(name=deviceName_1, poller=select.poll(), timeout = 5)
    keyboard = BTDevice(name=deviceName_2, poller=select.poll(), timeout = 5)

    # Track Drive, commonly known as tank drive
    tank = TankDrive()

    # Matplot Figure
    # https://stackoverflow.com/questions/24783530/python-realtime-plotting
    if DISPLAY:
        import matplotlib.pyplot as plt # this import is slow
        plt.ion()
        fig, ax = plt.subplots(1,1)
        hor     = ['Left', 'Right']
        ver     = [0, 0]
        bars    = ax.bar(hor, ver)
        ax.set_xlabel('Motor')
        ax.set_ylabel('Speed')
        ax.set_ylim(-30,30)
        fig.canvas.draw()
        fig.canvas.flush_events()

    # UDEV Monitor
    # Connection and disconnection monitor
    monitor_pollInterval = 1 
    monitorPoller  = select.poll()
    context =  pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='input')
    monitor.start()
    monitorPoller.register(monitor, 
                        select.POLLIN + select.POLLPRI + select.POLLHUP 
                        + select.POLLRDHUP + select.POLLNVAL + select.POLLERR )
                        # register all events except ready for output

    # Logging
    logging.basicConfig(level=logging.INFO) # options are: DEBUG, INFO, ERROR, WARNING
    logger = logging.getLogger("GamePad")

    # Initialize Variables
    last_inputTime   = time.perf_counter()
    last_monitorTime = time.perf_counter()

    #####################################################################
    # Check if desired devices are already connected to system
    #####################################################################
    udevices = context.list_devices(subsystem='input')                  # list all input devices
    for udev in udevices:
        if udev.device_node:                                            # only interested in devices with a device node
            if 'event' in udev.device_node:                             # only interested in event devices
                evdevice = InputDevice(udev.device_node)                # create event device
                if joystick.name == evdevice.name:                      # check if desired joystick was added          
                    joystick.path = evdevice.path                       # keep track of path
                    joystick.device = evdevice                          #
                    joystick.poller.register(evdevice, select.POLLIN)   # poller
                    logger.log(logging.INFO, "Observing Joystick {} at {} with {}.".format(evdevice.name,evdevice.path,evdevice.phys))
                elif keyboard.name == evdevice.name:                    # check if desired keyboard was added
                    keyboard.path = evdevice.path                       # keep track of path
                    keyboard.device = evdevice
                    keyboard.poller.register(evdevice, select.POLLIN)
                    logger.log(logging.INFO, "Observing Keyboard {} at {} with {}.".format(evdevice.name,evdevice.path,evdevice.phys))
                else:
                    logger.log(logging.INFO, "System Event Device found {} at {} with {}. Not observing.".format(evdevice.name,evdevice.path,evdevice.phys))
            else:
                logger.log(logging.INFO, "System Input Device found {} with type ({}). Not observing.".format(udev.device_node, udev.device_type))

    #####################################################################
    # Main Loop
    #####################################################################
    while True:

        current_time = time.perf_counter()

        #####################################################
        # Check if we had 'add' or 'disconnect' event in udev
        # disconnect is recognized after significant delay usually (not very useful)
        #####################################################
        if (current_time - last_monitorTime) > monitor_pollInterval : 
            last_monitorTime = current_time

            fdVsEvent = monitorPoller.poll(10)                          # timeout in milliseconds
            for descriptor, event in fdVsEvent:
                logger.log(logging.DEBUG, "Monitor Descriptor: {} Event: {}".format(descriptor,event))
                if descriptor == monitor.fileno(): 
                    for udev in iter(functools.partial(monitor.poll, 0), None):
                        if udev.device_node:                            # we're only interested in devices that have a device node
                            # Deal with Device Additions
                            # ##########################
                            if udev.action == 'add':
                                if 'event' in udev.device_node:         # only interested in event devices
                                    evdevice = InputDevice(udev.device_node)    # create event device
                                    if joystick.name == evdevice.name:  # check if desired joystick was added          
                                        joystick.path = evdevice.path   # keep track of path
                                        joystick.device = evdevice         
                                        joystick.poller.register(evdevice, select.POLLIN)
                                        logger.log(logging.INFO, "Observing Joystick {} at {} with {}.".format(evdevice.name,evdevice.path,evdevice.phys))
                                    elif keyboard.name == evdevice.name: # check if desired keyboard was added
                                        keyboard.path = evdevice.path   # keep track of path
                                        keyboard.device = evdevice
                                        keyboard.poller.register(evdevice, select.POLLIN)
                                        logger.log(logging.INFO, "Observing Keyboard {} at {} with {}.".format(evdevice.name,evdevice.path,evdevice.phys))
                                    else:
                                        logger.log(logging.INFO, "System Event Device found {} at {} with {}. Not observing.".format(evdevice.name,evdevice.path,evdevice.phys))
                                else:
                                    logger.log(logging.INFO, "System Input Device found {} with type ({}). Not observing.".format(udev.device_node, udev.device_type))
                            # Deal with Device Removals
                            # ##########################
                            elif udev.action == 'remove':
                                # check if joystick was removed
                                if udev.device_node == joystick.path:
                                    if joystick.device is not None:
                                        joystick.poller.unregister(joystick.device)
                                        joystick.path = ""
                                        joystick.device = None
                                        logger.log(logging.INFO, "Joystick {} removed.".format(joystick.name))
                                # check if keybaord was removed
                                elif udev.device_node == keyboard.path:
                                    logger.log(logging.INFO, "Keyboard {} removed.".format(keyboard.name))
                                    if keyboard.device is not None:
                                        keyboard.poller.unregister(keyboard.device)
                                    keyboard.path = ""
                                    keyboard.device = None
                                else:
                                    logger.log(logging.INFO, "Device {} removed.".format(udev.device_node))
                            else:
                                logger.log(logging.INFO, "Unknown Action {} from {}.".format(udev.action, udev.device_node))

        #####################################################
        # Check for input events
        # Disconnect detection is faster than with UDEV, but
        # cannot connect scan for new devices with evdev
        #####################################################

        if (current_time - last_inputTime) > input_pollInterval : 
            last_inputTime = current_time

            fdVsEvent = joystick.poller.poll(joystick.timeout)
            for descriptor, event in fdVsEvent:
                logger.log(logging.DEBUG, "Joystick Descriptor: {} Event: {}".format(descriptor, event))
                if event == select.POLLIN:
                    if joystick.device is not None:
                        for e in joystick.device.read():
                            handleEvent(event=e, tank=tank, logger=logger)
                elif event & select.POLLHUP:
                    logger.log(logging.INFO, "Joystick disconnected.")
                    joystick.poller.unregister(joystick.device)
                    joystick.device = None
            fdVsEvent = keyboard.poller.poll(keyboard.timeout)          # timeout in milliseconds
            for descriptor, event in fdVsEvent:
                logger.log(logging.DEBUG, "Keyboard Descriptor: {} Event: {}".format(descriptor,event))
                if event == select.POLLIN:
                    if keyboard.device is not None:
                        for e in keyboard.device.read():
                            handleEvent(event=e, tank=tank, logger=logger)
                elif event & select.POLLHUP:
                    logger.log(logging.INFO, "Keyboard disconnected.")
                    keyboard.poller.unregister(keyboard.device)
                    keyboard.device = None

        #####################################################
        # Display Speed
        ##################################################### 

        if DISPLAY:        
            hor = ['Left', 'Right']
            ver = [tank.speed_left, tank.speed_right]
            for bar,h in zip(bars,ver):
                bar.set_height(h)
            fig.canvas.draw()
            fig.canvas.flush_events()
