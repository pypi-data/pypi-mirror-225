import time
from typing import Optional, Tuple, Union
import functools

from .device import SerialDevice, check_initialized, check_serial


def check_axis_num(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        # could be a kwarg or arg
        if 'axis_number' in kwargs:
            axis_number = kwargs['axis_number']
        else:
            axis_number = args[0]
            
        if not self.is_axis_num_valid(axis_number):
            return (False, "Axis number is not valid or not part of passed tuple during construction.")
        return func(self, *args, **kwargs)
    return wrapper

class NewportESP301(SerialDevice):
    def __init__(
            self, 
            name: str,
            port: str,
            baudrate: int = 921600,
            timeout: Optional[float] = 1.0,
            axis_list: Tuple[int, ...] = (1,),
            default_speed: float = 20.0,
            poll_interval: float = 0.1):

        super().__init__(name, port, baudrate, timeout)
        self._axis_list = axis_list
        self._default_speed = default_speed #make list
        # self._default_speed_list = defaults_speed_list
        self._poll_interval = poll_interval
        self._max_speed = 200.0 # make list
        # self._max_speed_list = max_speed_list

    def get_init_args(self) -> dict:
        args_dict = {
            "name": self._name,
            "port": self._port,
            "baudrate": self._baudrate,
            "timeout": self._timeout,
            "axis_list": self._axis_list,
            "default_speed": self._default_speed,
            "poll_interval": self._poll_interval,
        }
        return args_dict

    def update_init_args(self, args_dict: dict):
        self._name = args_dict["name"]
        self._port = args_dict["port"]
        self._baudrate = args_dict["baudrate"]
        self._timeout = args_dict["timeout"]
        self._axis_list = args_dict["axis_list"]
        self._default_speed = args_dict["default_speed"]
        self._poll_interval = args_dict["poll_interval"]

    @property
    def default_speed(self) -> float:
        return self._default_speed

    @default_speed.setter
    def default_speed(self, speed: float):
        if speed > 0.0 and speed < self._max_speed:
            self._default_speed = speed

    # check_error already has serial check
    # easier to just set is_intialized False at the very beginning
    # do for all receivers
    def initialize(self) -> Tuple[bool, str]:
        # if not self.ser.is_open:
        #     return (False, "Serial port " + self._port + " is not open. ")

        was_successful, message = self.check_error() # just used to flush error and serial input buffer if there is an error
        if not was_successful:
            return (was_successful, message)

        self.ser.reset_input_buffer() # flush the serial input buffer even if there was no error

        for axis in self._axis_list:
            # Make sure axis motor is turned on
            was_turned_on, message = self.axis_on(axis)
            if not was_turned_on:
                self._is_initialized = False
                return (was_turned_on, message)
            # set units to mm, homing value to 0, set max speed, set current speed 
            command = str(axis) + "SN2;" + str(axis) + "SH0;" + str(axis) + "VU" + str(self._max_speed) + ";" + str(axis) + "VA" + str(self.default_speed) + "\r"
            self.ser.write(command.encode('ascii'))

        # Make sure initialization of settings was successful
        was_successful, message = self.check_error()
        if not was_successful:
            self._is_initialized = False
            return (was_successful, message)

        for axis in self._axis_list:
            was_homed, message = self.home(axis)
            if not was_homed:
                self._is_initialized = False
                return (was_homed, message)
    
        self._is_initialized = True
        return (True, "Successfully initialized axes by setting units to mm, settings max/current speeds, and homing. Current position set to zero.")

    # move_speed_absolute already has serial check
    def deinitialize(self, reset_init_flag: bool = True) -> Tuple[bool, str]:
        # if not self.ser.is_open:
        #     return (False, "Serial port " + self._port + " is not open. ")

        for axis in self._axis_list:
            was_zeroed, message = self.move_speed_absolute(0.0, speed=None, axis_number=axis)
            if not was_zeroed:
                return (was_zeroed, message)

        if reset_init_flag:
            self._is_initialized = False

        return (True, "Successfully deinitialized axes by moving to position zero.")

    # make a home_all function
    @check_serial
    def home(self, axis_number: int) -> Tuple[bool, str]:
        # if not self.ser.is_open:
        #     return (False, "Serial port " + self._port + " is not open. ")

        command = str(axis_number) + "OR4\r"
        self.ser.write(command.encode('ascii'))

        while self.is_any_moving():
            time.sleep(self._poll_interval)
        # pause one more time in case motor stopped moving but position has not been reset yet     
        time.sleep(self._poll_interval)

        was_successful, message = self.check_error()
        if not was_successful:
            return (was_successful, message)
        else:
            return (True, "Successfully homed axes " + str(axis_number))

    # Consider a decorator for checks?
    @check_serial
    @check_initialized
    @check_axis_num
    def move_speed_absolute(self, axis_number: int = 1, position: Optional[float] = None, speed: Optional[float] = None) -> Tuple[bool, str]:
        # if not self.ser.is_open:
        # #     return (False, "Serial port " + self._port + " is not open. ")
        # if not self.is_axis_num_valid(axis_number):
        #     return (False, "Axis number is not valid or not part of passed tuple during construction.")
        # if not self._is_initialized:
        #     return (False, "ESP301 axes are not initialized.")
        
        # I want axis number to be the first arg so the decorator can pick it up as arg[0]
        # but I also want axis_number to have a default value of 1, so position needs a default value now
        if position is None:
            return (False, "Position was not specified")

        if speed is None:
            speed = self._default_speed

        command = str(axis_number) + "VA" + str(speed) +"\r"
        self.ser.write(command.encode('ascii'))

        was_successful, message = self.check_error()
        if not was_successful:
            return (was_successful, message)

        if position >= 0.0:
            sign = "+"
        else:
            sign = "-"

        # removed the WS command because it causes timeouts when checking if moving 
        # command = str(axis_number) + "PA" + sign + str(abs(position)) + ";" + str(axis_number) + "WS\r"
        command = str(axis_number) + "PA" + sign + str(abs(position)) + "\r"
        self.ser.write(command.encode('ascii'))

        while self.is_moving(axis_number):
            time.sleep(self._poll_interval)

        was_successful, message = self.check_error()
        if not was_successful:
            return (was_successful, message)
        else:
            return (True, "Successfully completed absolute move at " + str(position))

    @check_serial
    @check_initialized
    @check_axis_num
    def move_speed_relative(self, axis_number: int = 1, distance: Optional[float] = None, speed: Optional[float] = None) -> Tuple[bool, str]:
        # if not self.ser.is_open:
        # #     return (False, "Serial port " + self._port + " is not open. ")
        # if not self.is_axis_num_valid(axis_number):
        #     return (False, "Axis number is not valid or not part of passed tuple during construction.")
        # if not self._is_initialized:
        #     return (False, "ESP301 axes are not initialized.")
        if distance is None:
            return (False, "Distance was not specified")
        
        if speed is None:
            speed = self._default_speed

        command = str(axis_number) + "VA" + str(speed) +"\r"
        self.ser.write(command.encode('ascii'))

        was_successful, message = self.check_error()
        if not was_successful:
            return (was_successful, message)

        if distance >= 0.0:
            sign = "+"
        else:
            sign = "-"

        # removed the WS command because it causes timeouts when checking if moving 
        # command = str(axis_number) + "PR" + sign + str(abs(distance)) + ";" + str(axis_number) + "WS\r"
        command = str(axis_number) + "PR" + sign + str(abs(distance)) + "\r"

        self.ser.write(command.encode('ascii'))

        while self.is_moving(axis_number):
            time.sleep(self._poll_interval)

        was_successful, message = self.check_error()
        if not was_successful:
            return (was_successful, message)
        else:
            return (True, "Successfully completed relative move by " + str(distance))
        

    def is_axis_num_valid(self, axis_number: int) -> bool:
        if axis_number in self._axis_list:
            return True
        else:
            return False
    
    # check axis num
    @check_serial
    @check_axis_num
    def is_moving(self, axis_number: int = 1) -> bool:
        # if not self.ser.is_open:
        #     return False
        # else:
        command = str(axis_number) + "MD?\r"
        self.ser.write(command.encode('ascii'))
        response = self.ser.readline()

        if response.strip().decode('ascii') == '0':
            # motion is not done = is moving
            return True
        else:
            # includes timeout case
            return False

    def is_any_moving(self) -> bool:
        is_moving_list = []
        for ndx, axis_number in enumerate(self._axis_list):
            command = str(axis_number) + "MD?\r"
            self.ser.write(command.encode('ascii'))
            response = self.ser.readline()

            if response.strip().decode('ascii') == '0':
                is_moving_list.append(True)
            else:
                is_moving_list.append(False)

        if any(is_moving_list):
            return True
        else: 
            return False

    @check_serial
    def check_error(self) -> Tuple[bool, str]:
        # not needed for queries, but use when instructing to do something
        
        # if not self.ser.is_open:
        #     return (False, "Serial port " + self._port + " is not open. ")

        command = "TB?\r"
        self.ser.write(command.encode('ascii'))
        response = self.ser.readline()

        if response == b'':
            return (False, "Response timed out.")
        
        response = response.strip().decode('ascii')

        if response[0] == '0':
            return (True, "No errors.")
        else:
            # flush the error buffer
            for n in range(10):
                self.ser.write(command.encode('ascii'))
                self.ser.readline()
            # flush the serial input buffer
            time.sleep(0.1)
            self.ser.reset_input_buffer()
            return (False, response)
    
    @check_serial
    @check_axis_num
    def position(self, axis_number: int = 1) -> Tuple[bool, Union[str, float]]:
        # if not self.ser.is_open:
        #     return (False, "Serial port " + self._port + " is not open. ")
        # if not self.is_axis_num_valid(axis_number):
        #     return (False, "Axis number is not valid or not part of passed tuple during construction.")

        command = str(axis_number) + "TP\r"
        self.ser.write(command.encode('ascii'))
        position_str = self.ser.readline()
        if position_str == b'':
            return (False, "Response timed out.")
        else:    
            return (True, float(position_str.strip().decode('ascii')))

    @check_serial
    @check_axis_num
    def axis_on(self, axis_number: int = 1) -> Tuple[bool, str]:
        # if not self.ser.is_open:
        #     return (False, "Serial port " + self._port + " is not open. ")
        # if not self.is_axis_num_valid(axis_number):
        #     return (False, "Axis number is not valid or not part of passed tuple during construction.")

        command = str(axis_number) + "MO\r"
        self.ser.write(command.encode('ascii'))

        was_successful, message = self.check_error()
        if not was_successful:
            return (was_successful, message)

        command = str(axis_number) + "MO?\r"
        self.ser.write(command.encode('ascii'))
        response = self.ser.readline()

        if response.strip().decode('ascii') == '1':
            return (True, "Axis " + str(axis_number) + " motor successfully turned ON.")
        else:
            # also means timeout
            return (False, "Axis " + str(axis_number) + " motor failed to turned ON.")

    @check_serial
    @check_axis_num
    def axis_off(self, axis_number: int = 1) -> Tuple[bool, str]:
        # if not self.ser.is_open:
        #     return (False, "Serial port " + self._port + " is not open. ")
        # if not self.is_axis_num_valid(axis_number):
        #     return (False, "Axis number is not valid or not part of passed tuple during construction.")

        command = str(axis_number) + "MF\r"
        self.ser.write(command.encode('ascii'))

        was_successful, message = self.check_error()
        if not was_successful:
            return (was_successful, message)

        command = str(axis_number) + "MF?\r"
        self.ser.write(command.encode('ascii'))
        response = self.ser.readline()

        if response.strip().decode('ascii') == '0':
            return (True, "Axis " + str(axis_number) + " motor successfully turned OFF.")
        else:
            # also means timeout
            return (False, "Axis " + str(axis_number) + " motor failed to turned OFF.")
