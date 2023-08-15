from commands.command import Command
from commands.utility_commands import LoopStartCommand, LoopEndCommand
from devices.heating_stage import HeatingStage
from devices.multi_stepper import MultiStepper
from devices.newport_esp301 import NewportESP301
from devices.festo_solenoid_valve import FestoSolenoidValve
from devices.ximea_camera import XimeaCamera
from devices.dummy_heater import DummyHeater
from devices.dummy_motor import DummyMotor
from devices.linear_stage_150 import LinearStage150
from devices.mts50_z8 import MTS50_Z8
from devices.keithley_2450 import Keithley2450
from devices.device import Device, MiscDeviceClass
from devices.utility_device import UtilityCommands

from commands.linear_stage_150_commands import *
from commands.mts50_z8_commands import *
from commands.dummy_heater_commands import *
from commands.dummy_motor_commands import *
from commands.dummy_meter_commands import *
from commands.keithley_2450_commands import *
from commands.festo_solenoid_valve_commands import *
from commands.ximea_camera_commands import *
from commands.utility_commands import *
from commands.heating_stage_commands import *
from commands.multi_stepper_commands import *
from commands.newport_esp301_commands import *
from commands.utility_commands import *

import json
import numpy as np
from typing import Tuple, Union


named_devices = {
    "PrintingStage": HeatingStage,
    "AnnealingStage": HeatingStage,
    "MultiStepper1": MultiStepper,
    "PrinterMotorX": NewportESP301,
    # "Spectrometer": StellarNetSpectrometer,
    "SampleCamera": XimeaCamera,
    "DummyHeater1": DummyHeater,
    "DummyHeater2": DummyHeater,
    "DummyMotor": DummyMotor,
    "DummyMotor1": DummyMotor,
    "DummyMotor2": DummyMotor,
}
command_directory = "commands/"
approved_devices = list(named_devices.keys())

# device_init_args = {
#     "DummyHeater": ["name", "heat_rate"],
#     "DummyMotor": ["name", "speed"],
# }


def dict_to_device(device: Device, type: str):
    device_cls = named_devices[type]
    arg_dict = device.get_init_args()

    # for attr in device_init_args[type]:
    #     arg_dict[attr] = dict["_"+attr]

    # print(arg_dict)
    return device_cls(**arg_dict)


def str_to_device(device_str: str):
    print(device_str)
    return eval(device_str)


def device_to_dict(device: Device):
    return device.get_init_args()


def evaluate(eval_str):
    return eval(eval_str)


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Device) or isinstance(obj, Command) or isinstance(obj, MiscDeviceClass):
            return obj.__dict__
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


heating_stage_ref = {
    "obj": HeatingStage,
    "serial": True,
    "serial_sequence": ["HeatingStageConnect", "HeatingStageInitialize"],
    "import_device": "from devices.heating_stage import HeatingStage",
    "import_commands": "from commands.heating_stage_commands import *",
    "init": {
        "default_code": "HeatingStage(name='Stage', port='', baudrate=115200, timeout=0.1, heating_timeout=600.0)",
        "obj_name": "HeatingStage",
        "args": {
            "name": {
                "default": "Stage",
                "type": str,
                "notes": "Name of the device",
            },
            "port": {"default": "COM", "type": str, "notes": "Port"},
            "baudrate": {
                "default": 115200,
                "type": int,
                "notes": "Baudrate",
            },
            "timeout": {
                "default": 0.1,
                "type": float,
                "notes": "Timeout",
            },
            "heating_timeout": {
                "default": 600.0,
                "type": float,
                "notes": "Heating timeout",
            },
        },
    },
    "commands": {
        "HeatingStageConnect": {
            "default_code": "HeatingStageConnect(receiver= '')",
            "args": {
                "receiver": {
                    "default": "Stage",
                    "type": str,
                    "notes": "Name of the device",
                }
            },
            "obj": HeatingStageConnect,
        },
        "HeatingStageInitialize": {
            "default_code": "HeatingStageInitialize(receiver= '')",
            "args": {
                "receiver": {
                    "default": "Stage",
                    "type": str,
                    "notes": "Name of the device",
                }
            },
            "obj": HeatingStageInitialize,
        },
        "HeatingStageDeinitialize": {
            "default_code": "HeatingStageDeinitialize(receiver= '')",
            "args": {
                "receiver": {
                    "default": "Stage",
                    "type": str,
                    "notes": "Name of the device",
                }
            },
            "obj": HeatingStageDeinitialize,
        },
        "HeatingStageSetTemp": {
            "default_code": "HeatingStageSetTemp(receiver= '', temperature= 0.0)",
            "args": {
                "receiver": {
                    "default": "Stage",
                    "type": str,
                    "notes": "Name of the device",
                },
                "temperature": {
                    "default": 0.0,
                    "type": float,
                    "notes": "Temperature",
                },
            },
            "obj": HeatingStageSetTemp,
        },
        "HeatingStageSetSetPoint": {
            "default_code": "HeatingStageSetSetPoint(receiver= '', temperature= 0.0)",
            "args": {
                "receiver": {
                    "default": "Stage",
                    "type": str,
                    "notes": "Name of the device",
                },
                "temperature": {
                    "default": 0.0,
                    "type": float,
                    "notes": "Temperature",
                },
            },
            "obj": HeatingStageSetSetPoint,
        },
    },
}


devices_ref_redundancy = {
    "UtilityCommands": {
        "obj": UtilityCommands,
        "serial": False,
        "import_device": "from devices.utility_commands import UtilityCommands",
        "import_commands": "from commands.utility_commands import *",
        "init": {
            "default_code": "# Utility Commands used",
            "obj_name": "UtilityCommands",
            "args": {},
        },
        "commands": {
            "LoopStartCommand": {
                "default_code": "LoopStartCommand()",
                "args": {},
                "obj": LoopStartCommand,
            },
            "LoopEndCommand": {
                "default_code": "LoopEndCommand()",
                "args": {},
                "obj": LoopEndCommand,
            },
            "DelayPauseCommand": {
                "default_code": "DelayPauseCommand(delay=0.0)",
                "args": {
                    "delay": {
                        "default": 0.0,
                        "type": float,
                        "notes": "Delay in seconds",
                    }
                },
                "obj": DelayPauseCommand,
            },
            "NotifySlackCommand": {
                "default_code": "NotifySlackCommand(message='Hello World')",
                "args": {
                    "message": {
                        "default": "Hello World",
                        "type": str,
                        "notes": "Message to send to slack",
                    }
                },
                "obj": NotifySlackCommand,
            },
            "LogUserMessageCommand": {
                "default_code": "LogUserMessageCommand(message='Hello World')",
                "args": {
                    "message": {
                        "default": "Hello World",
                        "type": str,
                        "notes": "Message to log",
                    }
                },
                "obj": LogUserMessageCommand,
            },
        },
    },
    "FestoSolenoidValve": {
        "obj": FestoSolenoidValve,
        "serial": True,
        "serial_sequence": ["FestoInitialize"],
        "import_device": "from devices.festo_solenoid_valve import FestoSolenoidValve",
        "import_commands": "from commands.festo_solenoid_valve_commands import *",
        "init": {
            "default_code": "FestoSolenoidValve(name='FestoSolenoidValve', numchannel=, port='COM5', baudrate=9600, timeout=0.1)",
            "obj_name": "FestoSolenoidValve",
            "args": {
                "name": {
                    "default": "FestoSolenoidValve",
                    "type": str,
                    "notes": "Name of the device.",
                },
                "numchannel": {
                    "default": 1,
                    "type": int,
                    "notes": "",
                },
                "port": {
                    "default": "COM5",
                    "type": str,
                    "notes": "Port",
                },
                "baudrate": {
                    "default": 9600,
                    "type": int,
                    "notes": "Baudrate",
                },
                "timeout": {
                    "default": 0.1,
                    "type": float,
                    "notes": "Timeout",
                },
            },
        },
        "commands": {
            "FestoInitialize": {
                "default_code": "FestoInitialize(receiver= '')",
                "args": {
                    "receiver": {
                        "default": "FestoSolenoidValve",
                        "type": str,
                        "notes": "Name of the device",
                    },
                },
                "obj": FestoInitialize,
            },
            "FestoDeinitialize": {
                "default_code": "FestoDeinitialize(receiver= '')",
                "args": {
                    "receiver": {
                        "default": "FestoSolenoidValve",
                        "type": str,
                        "notes": "Name of the device",
                    },
                },
                "obj": FestoDeinitialize,
            },
            "FestoValveOpen": {
                "default_code": "FestoValveOpen(receiver= '')",
                "args": {
                    "receiver": {
                        "default": "FestoSolenoidValve",
                        "type": str,
                        "notes": "Name of the device",
                    },
                },
                "obj": FestoValveOpen,
            },
            "FestoValveClosed": {
                "default_code": "FestoValveClosed(receiver= '')",
                "args": {
                    "receiver": {
                        "default": "FestoSolenoidValve",
                        "type": str,
                        "notes": "Name of the device",
                    },
                },
                "obj": FestoValveClosed,
            },
            "FestoOpenTimed": {
                "default_code": "FestoOpenTimed(receiver= '', time=0)",
                "args": {
                    "receiver": {
                        "default": "FestoSolenoidValve",
                        "type": str,
                        "notes": "Name of the device",
                    },
                    "time": {
                        "default": 0,
                        "type": int,
                        "notes": "Time to keep the valve open",
                    },
                },
                "obj": FestoOpenTimed,
            },
        },
    },
    "LinearStage150": {
        "obj": LinearStage150,
        "serial": True,
        "serial_sequence": ["LinearStage150Connect", "LinearStage150EnableMotor"],
        "import_device": "from devices.linear_stage_150 import LinearStage150",
        "import_commands": "from commands.linear_stage_150_commands import *",
        "telemetry": {
            "parameters": [
                {
                    "position": {
                        "function_name": "get_position()",
                        "data_type": "float",
                        "units": "mm",
                    }
                }
            ],
            "options": {"custom_init_args": ["port"]},
        },
        "init": {
            "default_code": "LinearStage150(name='LinearStage150', port='', baudrate=115200, timeout=0.1, destination=0x50, source=0x01, channel=1)",
            "obj_name": "LinearStage150",
            "args": {
                "name": {
                    "default": "LinearStage150",
                    "type": str,
                    "notes": "Name of the device.",
                },
                "port": {"default": "COM", "type": str, "notes": "Port"},
                "baudrate": {
                    "default": 115200,
                    "type": int,
                    "notes": "Baudrate",
                },
                "timeout": {
                    "default": 0.1,
                    "type": float,
                    "notes": "Timeout",
                },
                "destination": {
                    "default": 0x50,
                    "type": int,
                    "notes": "",
                },
                "source": {
                    "default": 0x01,
                    "type": int,
                    "notes": "",
                },
                "channel": {
                    "default": 1,
                    "type": int,
                    "notes": "",
                },
            },
        },
        "commands": {
            "LinearStage150Connect": {
                "default_code": "LinearStage150Connect(receiver= '')",
                "args": {
                    "receiver": {
                        "default": "LinearStage150",
                        "type": str,
                        "notes": "",
                    }
                },
                "obj": LinearStage150Connect,
            },
            "LinearStage150Initialize": {
                "default_code": "LinearStage150Initialize(receiver= '')",
                "args": {
                    "receiver": {
                        "default": "LinearStage150",
                        "type": str,
                        "notes": "",
                    }
                },
                "obj": LinearStage150Initialize,
            },
            "LinearStage150Deinitialize": {
                "default_code": "LinearStage150Deinitialize(receiver= '')",
                "args": {
                    "receiver": {
                        "default": "LinearStage150",
                        "type": str,
                        "notes": "",
                    }
                },
                "obj": LinearStage150Deinitialize,
            },
            "LinearStage150EnableMotor": {
                "default_code": "LinearStage150EnableMotor(receiver= '')",
                "args": {
                    "receiver": {
                        "default": "LinearStage150",
                        "type": str,
                        "notes": "",
                    }
                },
                "obj": LinearStage150EnableMotor,
            },
            "LinearStage150DisableMotor": {
                "default_code": "LinearStage150DisableMotor(receiver= '')",
                "args": {
                    "receiver": {
                        "default": "LinearStage150",
                        "type": str,
                        "notes": "",
                    }
                },
                "obj": LinearStage150DisableMotor,
            },
            "LinearStage150MoveAbsolute": {
                "default_code": "LinearStage150MoveAbsolute(receiver= '', position= 0)",
                "args": {
                    "receiver": {
                        "default": "LinearStage150",
                        "type": str,
                        "notes": "",
                    },
                    "position": {
                        "default": 0,
                        "type": int,
                        "notes": "",
                    },
                },
                "obj": LinearStage150MoveAbsolute,
            },
            "LinearStage150MoveRelative": {
                "default_code": "LinearStage150MoveRelative(receiver= '', distance= 0)",
                "args": {
                    "receiver": {
                        "default": "LinearStage150",
                        "type": str,
                        "notes": "",
                    },
                    "distance": {
                        "default": 0,
                        "type": int,
                        "notes": "",
                    },
                },
                "obj": LinearStage150MoveRelative,
            },
        },
    },
    "MTS50_Z8": {
        "obj": MTS50_Z8,
        "serial": True,
        "serial_sequence": ["MTS50_Z8Connect", "MTS50_Z8EnableMotor"],
        "import_device": "from devices.mts50_z8 import MTS50_Z8",
        "import_commands": "from commands.mts50_z8_commands import *",
        "init": {
            "default_code": "MTS50_Z8(name='MTS50_Z8', port='', baudrate=115200, timeout=0.1, destination=0x50, source=0x01, channel=1)",
            "obj_name": "MTS50_Z8",
            "args": {
                "name": {
                    "default": "MTS50_Z8",
                    "type": str,
                    "notes": "Name of the device.",
                },
                "port": {"default": "COM", "type": str, "notes": "Port"},
                "baudrate": {
                    "default": 115200,
                    "type": int,
                    "notes": "Baudrate",
                },
                "timeout": {
                    "default": 0.1,
                    "type": float,
                    "notes": "Timeout",
                },
                "destination": {
                    "default": 0x50,
                    "type": int,
                    "notes": "",
                },
                "source": {
                    "default": 0x01,
                    "type": int,
                    "notes": "",
                },
                "channel": {
                    "default": 1,
                    "type": int,
                    "notes": "",
                },
            },
        },
        "commands": {
            "MTS50_Z8Connect": {
                "default_code": "MTS50_Z8Connect(receiver= '')",
                "args": {
                    "receiver": {
                        "default": "MTS50_Z8",
                        "type": str,
                        "notes": "",
                    }
                },
                "obj": MTS50_Z8Connect,
            },
            "MTS50_Z8Initialize": {
                "default_code": "MTS50_Z8Initialize(receiver= '')",
                "args": {
                    "receiver": {
                        "default": "MTS50_Z8",
                        "type": str,
                        "notes": "",
                    }
                },
                "obj": MTS50_Z8Initialize,
            },
            "MTS50_Z8Deinitialize": {
                "default_code": "MTS50_Z8Deinitialize(receiver= '')",
                "args": {
                    "receiver": {
                        "default": "MTS50_Z8",
                        "type": str,
                        "notes": "",
                    }
                },
                "obj": MTS50_Z8Deinitialize,
            },
            "MTS50_Z8EnableMotor": {
                "default_code": "MTS50_Z8EnableMotor(receiver= '')",
                "args": {
                    "receiver": {
                        "default": "MTS50_Z8",
                        "type": str,
                        "notes": "",
                    }
                },
                "obj": MTS50_Z8EnableMotor,
            },
            "MTS50_Z8DisableMotor": {
                "default_code": "MTS50_Z8DisableMotor(receiver= '')",
                "args": {
                    "receiver": {
                        "default": "MTS50_Z8",
                        "type": str,
                        "notes": "",
                    }
                },
                "obj": MTS50_Z8DisableMotor,
            },
            "MTS50_Z8MoveAbsolute": {
                "default_code": "MTS50_Z8MoveAbsolute(receiver= '', position= 0)",
                "args": {
                    "receiver": {
                        "default": "MTS50_Z8",
                        "type": str,
                        "notes": "",
                    },
                    "position": {
                        "default": 0,
                        "type": int,
                        "notes": "",
                    },
                },
                "obj": MTS50_Z8MoveAbsolute,
            },
            "MTS50_Z8MoveRelative": {
                "default_code": "MTS50_Z8MoveRelative(receiver= '', distance= 0)",
                "args": {
                    "receiver": {
                        "default": "MTS50_Z8",
                        "type": str,
                        "notes": "",
                    },
                    "distance": {
                        "default": 0,
                        "type": int,
                        "notes": "",
                    },
                },
                "obj": MTS50_Z8MoveRelative,
            },
        },
    },
    "Keithley2450": {
        "obj": Keithley2450,
        "serial": True,
        "serial_sequence": ["Keithley2450Initialize"],
        "import_device": "from devices.keithley_2450 import Keithley2450",
        "import_commands": "from commands.keithley_2450_commands import *",
        "init": {
            "default_code": "Keithley2450(name='Keithley2450', ID='', query_delay=0)",
            "obj_name": "Keithley2450",
            "args": {
                "name": {
                    "default": "Keithley2450",
                    "type": str,
                    "notes": "Name of the device",
                },
                "ID": {
                    "default": "",
                    "type": str,
                    "notes": "ID of the device",
                },
                "query_delay": {
                    "default": 0,
                    "type": int,
                    "notes": "Delay between queries",
                },
            },
        },
        "commands": {
            "Keithley2450Initialize": {
                "default_code": "Keithley2450Initialize(receiver= '')",
                "args": {
                    "receiver": {
                        "default": "Keithley2450",
                        "type": str,
                        "notes": "",
                    }
                },
                "obj": Keithley2450Initialize,
            },
            "Keithley2450Deinitialize": {
                "default_code": "Keithley2450Deinitialize(receiver= '')",
                "args": {
                    "receiver": {
                        "default": "Keithley2450",
                        "type": str,
                        "notes": "",
                    }
                },
                "obj": Keithley2450Deinitialize,
            },
            "KeithleyWait": {
                "default_code": "KeithleyWait(receiver= '')",
                "args": {
                    "receiver": {
                        "default": "Keithley2450",
                        "type": str,
                        "notes": "",
                    }
                },
                "obj": KeithleyWait,
            },
            "KeithleyWriteCommand": {
                "default_code": "KeithleyWriteCommand(receiver= '', command= '')",
                "args": {
                    "receiver": {
                        "default": "Keithley2450",
                        "type": str,
                        "notes": "",
                    },
                    "command": {
                        "default": "",
                        "type": str,
                        "notes": "",
                    },
                },
                "obj": KeithleyWriteCommand,
            },
            "KeithleySetTerminal": {
                "default_code": "KeithleySetTerminal(receiver= '', position= 'front')",
                "args": {
                    "receiver": {
                        "default": "Keithley2450",
                        "type": str,
                        "notes": "",
                    },
                    "position": {
                        "default": "front",
                        "type": str,
                        "notes": "",
                    },
                },
                "obj": KeithleySetTerminal,
            },
            "KeithleyErrorCheck": {
                "default_code": "KeithleyErrorCheck(receiver= '')",
                "args": {
                    "receiver": {
                        "default": "Keithley2450",
                        "type": str,
                        "notes": "",
                    }
                },
                "obj": KeithleyErrorCheck,
            },
            "KeithleyClearBuffer": {
                "default_code": "KeithleyClearBuffer(receiver= '', buffer='defbuffer1')",
                "args": {
                    "receiver": {
                        "default": "Keithley2450",
                        "type": str,
                        "notes": "",
                    },
                    "buffer": {
                        "default": "defbuffer1",
                        "type": str,
                        "notes": "",
                    },
                },
                "obj": KeithleyClearBuffer,
            },
            "KeithleyIVCharacteristic": {
                "default_code": "KeithleyIVCharacteristic(receiver= '', ilimit=0.0, vmin=0.0, vmax=0.0, delay=0.0, steps=60)",
                "args": {
                    "receiver": {
                        "default": "Keithley2450",
                        "type": str,
                        "notes": "",
                    },
                    "ilimit": {
                        "default": 0.0,
                        "type": float,
                        "notes": "",
                    },
                    "vmin": {
                        "default": 0.0,
                        "type": float,
                        "notes": "",
                    },
                    "vmax": {
                        "default": 0.0,
                        "type": float,
                        "notes": "",
                    },
                    "delay": {
                        "default": 0.0,
                        "type": float,
                        "notes": "",
                    },
                    "steps": {
                        "default": 60,
                        "type": int,
                        "notes": "",
                    },
                },
                "obj": KeithleyIVCharacteristic,
            },
            "KeithleyFourPoint": {
                "default_code": "KeithleyFourPoint(receiver= '', test_curr=0.0, vlimit=0.0, curr_reversal = False)",
                "args": {
                    "receiver": {
                        "default": "Keithley2450",
                        "type": str,
                        "notes": "",
                    },
                    "test_curr": {
                        "default": 0.0,
                        "type": float,
                        "notes": "",
                    },
                    "vlimit": {
                        "default": 0.0,
                        "type": float,
                        "notes": "",
                    },
                    "curr_reversal": {
                        "default": False,
                        "type": bool,
                        "notes": "",
                    },
                },
                "obj": KeithleyFourPoint,
            },
            "KeithleyGetData": {
                "default_code": "KeithleyGetData(receiver= '', filename=None, four_point= False)",
                "args": {
                    "receiver": {
                        "default": "Keithley2450",
                        "type": str,
                        "notes": "",
                    },
                    "filename": {
                        "default": None,
                        "type": str,
                        "notes": "",
                    },
                    "four_point": {
                        "default": False,
                        "type": bool,
                        "notes": "",
                    },
                },
                "obj": KeithleyGetData,
            },
        },
    },
    "PrintingStage": heating_stage_ref,
    "AnnealingStage": heating_stage_ref,
    "MultiStepper": {
        "obj": MultiStepper,
        "serial": True,
        "serial_sequence": ["MultiStepperConnect", "MultiStepperInitialize"],
        "import_device": "from devices.multi_stepper import MultiStepper",
        "import_commands": "from commands.multi_stepper_commands import *",
        "init": {
            "default_code": "MultiStepper(name='MultiStepper', port='', baudrate=115200, timeout=0.1, destination=0x50, source=0x01, channel=1)",
            "obj_name": "MultiStepper",
            "args": {
                "name": {
                    "default": "MultiStepper",
                    "type": str,
                    "notes": "Name of the device",
                },
                "port": {
                    "default": "COM",
                    "type": str,
                    "notes": "Port of the device",
                },
                "baudrate": {
                    "default": 115200,
                    "type": int,
                    "notes": "Baudrate of the device",
                },
                "timeout": {
                    "default": 1.0,
                    "type": float,
                    "notes": "Timeout of the device",
                },
                "stepper_list": {
                    "default": (1,),
                    "type": Tuple[int, ...],
                    "notes": "List of stepper numbers",
                },
                "move_timeout": {
                    "default": 30.0,
                    "type": float,
                    "notes": "Timeout for move commands",
                },
            },
        },
        "commands": {
            "MultiStepperConnect": {
                "default_code": "MultiStepperConnect(receiver= '')",
                "args": {
                    "receiver": {
                        "default": "MultiStepper",
                        "type": str,
                        "notes": "Name of the device",
                    }
                },
                "obj": MultiStepperConnect,
            },
            "MultiStepperInitialize": {
                "default_code": "MultiStepperInitialize(receiver= '')",
                "args": {
                    "receiver": {
                        "default": "MultiStepper",
                        "type": str,
                        "notes": "Name of the device",
                    }
                },
                "obj": MultiStepperInitialize,
            },
            "MultiStepperDeinitialize": {
                "default_code": "MultiStepperDeinitialize(receiver= '')",
                "args": {
                    "receiver": {
                        "default": "MultiStepper",
                        "type": str,
                        "notes": "Name of the device",
                    }
                },
                "obj": MultiStepperDeinitialize,
            },
            "MultiStepperMoveAbsolute": {
                "default_code": "MultiStepperMoveAbsolute(receiver= '', stepper_number= 0, position= 0)",
                "args": {
                    "receiver": {
                        "default": "MultiStepper",
                        "type": str,
                        "notes": "Name of the device",
                    },
                    "stepper_number": {
                        "default": 0,
                        "type": int,
                        "notes": "Number of the stepper",
                    },
                    "position": {
                        "default": 0.0,
                        "type": float,
                        "notes": "Position to move to",
                    },
                },
                "obj": MultiStepperMoveAbsolute,
            },
            "MultiStepperMoveRelative": {
                "default_code": "MultiStepperMoveRelative(receiver= '', stepper_number= 0, distance= 0)",
                "args": {
                    "receiver": {
                        "default": "MultiStepper",
                        "type": str,
                        "notes": "Name of the device",
                    },
                    "stepper_number": {
                        "default": 0,
                        "type": int,
                        "notes": "Number of the stepper",
                    },
                    "distance": {
                        "default": 0.0,
                        "type": float,
                        "notes": "Distance to move",
                    },
                },
                "obj": MultiStepperMoveRelative,
            },
        },
    },
    "NewportESP301": {
        "obj": NewportESP301,
        "serial": True,
        "serial_sequence": ["NewportESP301Connect", "NewportESP301Initialize"],
        "import_device": "from devices.newport_esp301 import NewportESP301",
        "import_commands": "from commands.newport_esp301_commands import *",
        "init": {
            "default_code": "NewportESP301(name='NewportESP301', port='', baudrate=921600, timeout=1.0, axis_list = (1,), default_speed=20.0, poll_interval=0.1)",
            "obj_name": "NewportESP301",
            "args": {
                "name": {
                    "default": "NewportESP301",
                    "type": str,
                    "notes": "Name of the device",
                },
                "port": {
                    "default": "COM",
                    "type": str,
                    "notes": "Port of the device",
                },
                "baudrate": {
                    "default": 921600,
                    "type": int,
                    "notes": "Baudrate of the device",
                },
                "timeout": {
                    "default": 1.0,
                    "type": float,
                    "notes": "Timeout of the device",
                },
                "axis_list": {
                    "default": (1,),
                    "type": Tuple[int, ...],
                    "notes": "List of axis numbers",
                },
                "default_speed": {
                    "default": 20.0,
                    "type": float,
                    "notes": "Default speed of the device",
                },
                "poll_interval": {
                    "default": 0.1,
                    "type": float,
                    "notes": "Poll interval of the device",
                },
            },
        },
        "commands": {
            "NewportESP301Connect": {
                "default_code": "NewportESP301Connect(receiver= '')",
                "args": {
                    "receiver": {
                        "default": "NewportESP301",
                        "type": str,
                        "notes": "Name of the device",
                    }
                },
                "obj": NewportESP301Connect,
            },
            "NewportESP301Initialize": {
                "default_code": "NewportESP301Initialize(receiver= '')",
                "args": {
                    "receiver": {
                        "default": "NewportESP301",
                        "type": str,
                        "notes": "Name of the device",
                    }
                },
                "obj": NewportESP301Initialize,
            },
            "NewportESP301Deinitialize": {
                "default_code": "NewportESP301Deinitialize(receiver= '')",
                "args": {
                    "receiver": {
                        "default": "NewportESP301",
                        "type": str,
                        "notes": "Name of the device",
                    }
                },
                "obj": NewportESP301Deinitialize,
            },
            "NewportESP301MoveSpeedAbsolute": {
                "default_code": "NewportESP301MoveSpeedAbsolute(receiver= '', axis= 1, position= 0, speed= 20.0)",
                "args": {
                    "receiver": {
                        "default": "NewportESP301",
                        "type": str,
                        "notes": "Name of the device",
                    },
                    "axis": {
                        "default": 1,
                        "type": int,
                        "notes": "Axis number",
                    },
                    "position": {
                        "default": 0.0,
                        "type": float,
                        "notes": "Position to move to",
                    },
                    "speed": {
                        "default": 20.0,
                        "type": float,
                        "notes": "Speed to move at",
                    },
                },
                "obj": NewportESP301MoveSpeedAbsolute,
            },
            "NewportESP301MoveSpeedRelative": {
                "default_code": "NewportESP301MoveSpeedRelative(receiver= '', axis= 1, distance= 0, speed= 20.0)",
                "args": {
                    "receiver": {
                        "default": "NewportESP301",
                        "type": str,
                        "notes": "Name of the device",
                    },
                    "axis": {
                        "default": 1,
                        "type": int,
                        "notes": "Axis number",
                    },
                    "distance": {
                        "default": 0.0,
                        "type": float,
                        "notes": "Distance to move",
                    },
                    "speed": {
                        "default": 20.0,
                        "type": float,
                        "notes": "Speed to move at",
                    },
                },
                "obj": NewportESP301MoveSpeedRelative,
            },
        },
    },
    "DummyMotor": {
        "obj": DummyMotor,
        "serial": True,
        "serial_sequence": ["DummyMotorInitialize"],
        "import_device": "from devices.dummy_motor import DummyMotor",
        "import_commands": "from commands.dummy_motor_commands import *",
        "init": {
            "default_code": "DummyMotor(name='DummyMotor', speed=20.0)",
            "obj_name": "DummyMotor",
            "args": {
                "name": {
                    "default": "DummyMotor",
                    "type": str,
                    "notes": "Name of the device.",
                },
                "speed": {
                    "default": 20.0,
                    "type": float,
                    "notes": "Speed of the motor.",
                },
            },
        },
        "commands": {
            "DummyMotorInitialize": {
                "default_code": "DummyMotorInitialize(receiver= '')",
                "args": {
                    "receiver": {
                        "default": "DummyMotor",
                        "type": str,
                        "notes": "Name of the device.",
                    }
                },
                "obj": DummyMotorInitialize,
            },
            "DummyMotorDeinitialize": {
                "default_code": "DummyMotorDeinitialize(receiver= '')",
                "args": {
                    "receiver": {
                        "default": "DummyMotor",
                        "type": str,
                        "notes": "Name of the device.",
                    }
                },
                "obj": DummyMotorDeinitialize,
            },
            "DummyMotorSetSpeed": {
                "default_code": "DummyMotorSetSpeed(receiver= '', speed= 0.0)",
                "args": {
                    "receiver": {
                        "default": "DummyMotor",
                        "type": str,
                        "notes": "Name of the device.",
                    },
                    "speed": {
                        "default": 0.0,
                        "type": float,
                        "notes": "Speed of the motor.",
                    },
                },
                "obj": DummyMotorSetSpeed,
            },
            "DummyMotorMoveAbsolute": {
                "default_code": "DummyMotorMoveAbsolute(receiver= '', position= 0)",
                "args": {
                    "receiver": {
                        "default": "DummyMotor",
                        "type": str,
                        "notes": "Name of the device.",
                    },
                    "position": {
                        "default": 0,
                        "type": float,
                        "notes": "Position to move to.",
                    },
                },
                "obj": DummyMotorMoveAbsolute,
            },
            "DummyMotorMoveRelative": {
                "default_code": "DummyMotorMoveRelative(receiver= '', distance= 0)",
                "args": {
                    "receiver": {
                        "default": "DummyMotor",
                        "type": str,
                        "notes": "Name of the device.",
                    },
                    "distance": {
                        "default": 0,
                        "type": float,
                        "notes": "Distance to move.",
                    },
                },
                "obj": DummyMotorMoveRelative,
            },
            "DummyMotorMoveSpeedAbsolute": {
                "default_code": "DummyMotorMoveSpeedAbsolute(receiver= '', position= 0.0, speed= 0.0)",
                "args": {
                    "receiver": {
                        "default": "DummyMotor",
                        "type": str,
                        "notes": "Name of the device.",
                    },
                    "position": {
                        "default": 0.0,
                        "type": float,
                        "notes": "Position to move to.",
                    },
                    "speed": {
                        "default": 0.0,
                        "type": float,
                        "notes": "Speed of the motor.",
                    },
                },
                "obj": DummyMotorMoveSpeedAbsolute,
            },
        },
    },
    # "Spectrometer": {"obj": StellarNetSpectrometer},
    # "XimeaCamera": {"obj": XimeaCamera},
    "DummyHeater": {
        "obj": DummyHeater,
        "serial": True,
        "serial_sequence": ["DummyHeaterInitialize"],
        "import_device": "from devices.dummy_heater import DummyHeater",
        "import_commands": "from commands.dummy_heater_commands import *",
        "init": {
            "default_code": "DummyHeater(name='DummyHeater', heat_rate=20.0)",
            "obj_name": "DummyHeater",
            "args": {
                "name": {
                    "default": "DummyHeater",
                    "type": str,
                    "notes": "Name of the device.",
                },
                "heat_rate": {
                    "default": 20.0,
                    "type": float,
                    "notes": "Heat rate of the heater.",
                },
            },
        },
        "commands": {
            "DummyHeaterInitialize": {
                "default_code": "DummyHeaterInitialize(receiver= '')",
                "args": {
                    "receiver": {
                        "default": "DummyHeater",
                        "type": str,
                        "notes": "Name of the device.",
                    }
                },
                "obj": DummyHeaterInitialize,
            },
            "DummyHeaterDeinitialize": {
                "default_code": "DummyHeaterDeinitialize(receiver= '')",
                "args": {
                    "receiver": {
                        "default": "DummyHeater",
                        "type": str,
                        "notes": "Name of the device.",
                    }
                },
                "obj": DummyHeaterDeinitialize,
            },
            "DummyHeaterSetHeatRate": {
                "default_code": "DummyHeaterSetHeatRate(receiver= '', heat_rate= 0.0)",
                "args": {
                    "receiver": {
                        "default": "DummyHeater",
                        "type": str,
                        "notes": "Name of the device.",
                    },
                    "heat_rate": {
                        "default": 0.0,
                        "type": float,
                        "notes": "Heat rate of the heater.",
                    },
                },
                "obj": DummyHeaterSetHeatRate,
            },
            "DummyHeaterSetTemp": {
                "default_code": "DummyHeaterSetTemp(receiver= '', temperature= 0.0)",
                "args": {
                    "receiver": {
                        "default": "DummyHeater",
                        "type": str,
                        "notes": "Name of the device.",
                    },
                    "temperature": {
                        "default": 0.0,
                        "type": float,
                        "notes": "Temperature to set the heater to.",
                    },
                },
                "obj": DummyHeaterSetTemp,
            },
        },
    },
}


# devices_ref = {
#     "PrintingStage": heating_stage_ref,
#     "AnnealingStage": heating_stage_ref,
#     "MultiStepper": {
#         "obj": MultiStepper,
#         "import_device": "from devices.multi_stepper import MultiStepper",
#         "import_commands": "from commands.multi_stepper_commands import *",
#         "init": "MultiStepper(name='MultiStepper', port='', baudrate=115200, timeout=0.1, destination=0x50, source=0x01, channel=1)",
#         "commands": {
#             "MultiStepperConnect": "MultiStepperConnect(receiver= '')",
#             "MultiStepperInitialize": "MultiStepperInitialize(receiver= '')",
#             "MultiStepperDeinitialize": "MultiStepperDeinitialize(receiver= '')",
#             "MultiStepperMoveAbsolute": "MultiStepperMoveAbsolute(receiver= '', stepper_number= 0, position= 0)",
#             "MultiStepperMoveRelative": "MultiStepperMoveRelative(receiver= '', stepper_number= 0, distance= 0)",
#         },
#     },
#     "PrinterMotorX": {"obj": NewportESP301},
#     # "Spectrometer": {"obj": StellarNetSpectrometer},
#     "XimeaCamera": {"obj": XimeaCamera},
#     "DummyHeater": {"obj": DummyHeater},
#     "DummyMotor": {"obj": DummyMotor},
#     "LinearStage150": {
#         "obj": LinearStage150,
#         "import_device": "from devices.linear_stage_150 import LinearStage150",
#         "import_commands": "from commands.linear_stage_150_commands import *",
#         "init": "LinearStage150(name='LinearStage150', port='', baudrate=115200, timeout=0.1, destination=0x50, source=0x01, channel=1)",
#         "commands": {
#             "LinearStage150Connect": "LinearStage150Connect(receiver= '')",
#             "LinearStage150Initialize": "LinearStage150Initialize(receiver= '')",
#             "LinearStage150Deinitialize": "LinearStage150Deinitialize(receiver= '')",
#             "LinearStage150EnableMotor": "LinearStage150EnableMotor(receiver= '')",
#             "LinearStage150DisableMotor": "LinearStage150DisableMotor(receiver= '')",
#             "LinearStage150MoveAbsolute": "LinearStage150MoveAbsolute(receiver= '', position= 0)",
#             "LinearStage150MoveRelative": "LinearStage150MoveRelative(receiver= '', distance= 0)",
#         },
#     },
# }
