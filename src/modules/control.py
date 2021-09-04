# Copyright 2021 Chase Kidder

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

# modules/old_control.py

# https://pimylifeup.com/xbox-controllers-raspberry-pi/
# https://github.com/FRC4564/Xbox

# XBox one https://atar-axis.github.io/xpadneo/
# XBox 360 https://github.com/linusg/xbox360controller
# Xpad mapping https://github.com/torvalds/linux/blob/master/include/uapi/linux/input-event-codes.h
# Xpad docs https://www.kernel.org/doc/Documentation/input/xpad.txt
# https://wiki.unity3d.com/index.php?title=Xbox360Controller

import modules.drive as drive

from inputs import devices, get_gamepad
import time

#robot = drive.DriveTrain()



class LED_MODE:
    BLINK = 1
    TOP_LEFT_BLINK_ON = 2
    TOP_RIGHT_BLINK_ON = 3
    BOTTOM_LEFT_BLINK_ON = 4
    BOTTOM_RIGHT_BLINK_ON = 5
    TOP_LEFT_ON = 6
    OFF = 0
    TOP_RIGHT_ON = 7
    BOTTOM_LEFT_ON = 8
    BOTTOM_RIGHT_ON = 9
    ROTATE = 10
    BLINK_PREV = 11
    BLINK_SLOW_PREV = 12
    ROTATE_TWO = 13
    BLINK_SLOW = 14
    BLINK_ONCE_PREV = 15


class controller():
    def __init__(self) -> None:
        self.__controller = devices.gamepads[0]
        self.buttons = {
            "BTN_START": 0,
            "BTN_MODE": 0,
            "BTN_SELECT": 0,
            "BTN_NORTH": 0,
            "BTN_SOUTH": 0,
            "BTN_EAST": 0,
            "BTN_WEST": 0,
            "BTN_TR": 0,
            "BTN_TL": 0,
            "BTN_THUMBL": 0,
            "BTN_THUMBR": 0,
            "ABS_HAT0Y": 0, # -1 = UP, 1 = Down
            "ABS_HAT0X": 0, # -1 = Left, 1 = Right
            "ABS_Z": 0, # 0-255
            "ABS_RZ": 0, # 0-255
            "ABS_Y": 0, # - = Up, + = Down, -32768 - 32768
            "ABS_X": 0, # - = Left, + = Right, -32768 - 32768
            "ABS_RY": 0, # - = Up, + = Down, -32768 - 32768
            "ABS_RX": 0, # - = Left, + = Right, -32768 - 32768
        }

        print(self.__controller)
        

    def rumble(self) -> None:
        # Rumble for 0.5 seconds at 50% on each side
        if self.__controller.has_rumble:
            self.__controller.set_rumble(0.5, 0.5, 0.5)
        

    def LED(self, mode:int) -> None:
        if self.__controller.has_led:
            self.__controller.set_led(mode)
            time.sleep(1)


    def get_buttons(self) -> None:
        events = get_gamepad()
        for event in events:
            if event.ev_type == "Key":
                print(event.code, event.state)
                self.keys[event.code] = event.state
        
