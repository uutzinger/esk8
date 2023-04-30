#!/usr/bin/env python3
#####################################################################
# Read Gamepad with Connect and Disconnect
# Urs Utzinger
# 2023
#####################################################################
# Event masks are
# POLLIN    1 data available to read
# POLLPRI   2 urgent data to read
# POLLOUT   4 ready for output
# POLLERR   8 error conditions of some sort
# POLLHUP   16 hung up
# POLLNVAL  32 invalid request
# POLLRDHUP 8192 peer closed connected 
# e.g. pollerObject.register(monitor, select.POLLIN)
#####################################################################

DISPLAY = True # Will display speed in figure

# Imports
import functools
import pyudev
import select
import time
import logging
import matplotlib.pyplot as plt
from evdev import InputDevice, categorize, ecodes

#####################################################################
# Utility functions
#####################################################################
def clamp(val: cython.double, smallest: cython.double, largest: cython.double): 
    '''
    Clip val to [smallest, largest]
    '''
    if val < smallest: return smallest
    if val > largest: return largest
    return val

def handleEvent(event=None, tank=None):
    # Gamepad Keys
    #####################################################################
    # Joystick
    # REL_X         -7(left) ... +7(right)
    # REL_Y         -7(up)   ... +7(down)
    # BTN_LEFT       pushed value 1, released 0, large front button and also button A
    # Keys
    # KEY_ESC        pushed value 1, continuous 2, released 0 Second button and button B
    # KEY_VOLUMEUP   pushed value 1, continuous 2, released 0 Button C
    # KEY_VOLUMEDOWN pushed value 1, continuous 2, released 0 Button D
    #####################################################################
    # event.type
    # event.code
    # event.value
    #####################################################
    # Example of input events for joystick, key and button
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
    if event is not None:
        if event.type == ecodes.EV_REL:
            if event.code == ecodes.ecodes['REL_X']:
                if tank is not None:
                    # steer left or right
                    tank.update(REL_X=event.value)
                    pass
            elif event.code == ecodes.ecodes['REL_Y']:
                if tank is not None:
                    # go faster or slower
                    tank.update(REL_Y=event.value)
        elif event.type == ecodes.EV_KEY:
            if event.code == ecodes.ecodes['KEY_ESC']:
                # steer center
                if tank is not None:
                    tank.center()
            elif event.code == ecodes.ecodes['KEY_VOLUMEUP']:
                # Show battery
                pass # button D was selected
            elif event.code == ecodes.ecodes['KEY_VOLUMEDOWN']:
                # Show lights/speed
                pass # button C was selected
        elif event.type == ecodes.EV_BTN:
            if event.code == ecodes.ecodes['BTN_LEFT']:
                # toggles turbo / eco mode
                # Need to check for value going to 1 and then to 0 and then changing turbo
                if tank is not None:
                    tank.turbo()
        else:
            pass

#####################################################################
# Classes
#####################################################################

# Keep  track of bluetooth device
class BTDevice(object):
    def __init__(self, name="", path="", device=None, poller=None, timeout=5):
        self.name    = name
        self.path    = path
        self.device  = device
        self.poller  = poller    
        self.timeout = timeout  # poller timeout in milliseconds

class TankDrive(object):
        ###########
    # Tank Drive
    # speed: speed base 
    # left_right:  left versus right -1..+1
    # speed_Left:  set speed for left motor
    # speed_Right: set speed for right motor
    ###########

    def __init__(self):
        self.MAXUPDOWN     =  7 # max joystick value, needs to be positive
        self.MINUPDOWN     = -7 # min joystick value, needs to be negative
        self.MAXLR         =  7 
        self.MINLR         = -7 
        self.SENS          = 1.5 # non linear joystick sensitivity
        self.MAX_SPEED     =  30 # max speed value
        self.MIN_SPEED     = -30
        self.MAX_RATIO     =  1.
        self.MIN_RATIO     = -1.
        self.SPEED_GAIN    = 0.1 # how fast to increase/decrease speed
        self.RATIO_GAIN    = 0.1 # how fast to steer
        self.speed         = 0   # set speed to zero
        self.reatio        = 0   # set steering straight
        self.speed_left    = 0   # set left & right zero
        self.speed_right   = 0
        self.eco           = True

    def update(self, REL_X=0, REL_Y=0):
        # Joystick conversion
        # Will create values between -1 and 1
        # non linear adjustments

        if REL_Y < 0:
            _up_down    = - (REL_Y/MINUPDOWN)^SENS # -1..1
        else: 
            _up_down    =   (REL_Y/MAXUPDOWN)^SENS
        if REL_X < 0:
            _left_right = - (REL_X/MINLR)^SENS     # -1..1
        else:
            _left_right =   (REL_X/MAXLR)^SENS     # -1..1

        # Set speed will be adjusted incrementally by joystick value
        # Speed is clamped
        self.speed   += (self.SPEED_GAIN * _up_down)
        self.speed = clamp(self.speed, self.MIN_SPEED, self.MAX_SPEED)

        # Left-Right ratio
        self.ratio  += (self.RATIO_GAIN * left_right)
        self.ratio = clamp(self.ratio, self.MIN_RATIO, self.MAX_RATIO)

        # Left versus right motor
        # if ratio is -1 left motor is 0 and right motor is 2 * speed
        self.speed_left  = self.speed + self.speed *self.ratio
        self.speed_right = self.speed - self.speed *self.ratio

    def turbo(self):
        if self.eco:
            self.eco=True
            self.SPEED_GAIN = 0.2
        else:
            self.eco=False
            self.SPEED_GAIN = 0.1

    def center(self):
        self.ratio = 0

#####################################################################
# Setup
#####################################################################

# Input devices to be watched
# Keypad and Joystick
input_pollInterval = 0.001 # how long to wait for next poll
joystick = BTDevice(name="Umido ESoul DH2 Mouse",    poller=select.poll(), timeout = 5)
keyboard = BTDevice(name="Umido ESoul DH2 Keyboard", poller=select.poll(), timeout = 5)

# Tank Drive
tank = TankDrive()

# Matplot Figure
if DISPLAY:
    fig = plt.figure()    
    fig.title('Speed')
    fig.xlabel('Motor')
    fig.ylabel('Speed')
    fig.ion()

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
    #####################################################

    if (current_time - last_inputTime) > input_pollInterval : 
        last_inputTime = current_time

        fdVsEvent = joystick.poller.poll(joystick.timeout)
        for descriptor, event in fdVsEvent:
            logger.log(logging.DEBUG, "Joystick Descriptor: {} Event: {}".format(descriptor, event))
            if event == select.POLLIN:
                if joystick.device is not None:
                    for e in joystick.device.read():
                        # Convert code, type in names
                        print("Type: {}, Code: {}, Value: {}".format(ecodes.EV[e.type], ecodes.bytype[e.type][e.code], e.value))
                        handleEvent(event=e, tank=tank)
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
                        print("Type: {}, Code: {}, Value: {}".format(ecodes.EV[e.type], ecodes.bytype[e.type][e.code], e.value))
                        handleEvent(event=e, tank=tank)
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
            fig.cla()
            fig.bar(hor, ver)
            fig.show(block=False)
            