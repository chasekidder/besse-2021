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

# modules/control.py

# https://pimylifeup.com/xbox-controllers-raspberry-pi/
# https://github.com/FRC4564/Xbox

# XBox one https://atar-axis.github.io/xpadneo/
# XBox 360 https://github.com/linusg/xbox360controller
# Xpad mapping https://github.com/torvalds/linux/blob/master/include/uapi/linux/input-event-codes.h
# Xpad docs https://www.kernel.org/doc/Documentation/input/xpad.txt
# https://wiki.unity3d.com/index.php?title=Xbox360Controller

from xbox360controller import Xbox360Controller
import time

CONTROLLER_ID = 0

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
        self.__controller = Xbox360Controller(
            index=CONTROLLER_ID, 
            axis_threshold=0.2, 
            raw_mode=False
            )

        print(self.__controller.info())

        self.__controller.button_select.when_pressed = self.__select_button_pressed
        self.__controller.button_mode.when_pressed = self.__mode_button_pressed
        self.__controller.button_start.when_pressed = self.__start_button_pressed
        self.__controller.button_a.when_pressed = self.__A_button_pressed
        self.__controller.button_b.when_pressed = self.__B_button_pressed
        self.__controller.button_x.when_pressed = self.__X_button_pressed
        self.__controller.button_y.when_pressed = self.__Y_button_pressed
        self.__controller.button_trigger_l.when_pressed = self.__L_trigger_pressed
        self.__controller.button_trigger_r.when_pressed = self.__R_trigger_pressed
        self.__controller.button_thumb_l.when_pressed = self.__L_shoulder_pressed
        self.__controller.button_thumb_r.when_pressed = self.__R_shoulder_pressed

        self.__controller.button_select.when_released = self.__select_button_released
        self.__controller.button_mode.when_released = self.__mode_button_released
        self.__controller.button_start.when_released = self.__start_button_released
        self.__controller.button_a.when_released = self.__A_button_released
        self.__controller.button_b.when_released = self.__B_button_released
        self.__controller.button_x.when_released = self.__X_button_released
        self.__controller.button_y.when_released = self.__Y_button_released
        self.__controller.button_trigger_l.when_released= self.__L_trigger_released
        self.__controller.button_trigger_r.when_released = self.__R_trigger_released
        self.__controller.button_thumb_l.when_released = self.__L_shoulder_released
        self.__controller.button_thumb_r.when_released = self.__R_shoulder_released

        self.__controller.axis_l.when_moved = self.__axis_moved
        self.__controller.axis_r.when_moved = self.__axis_moved

    def rumble(self) -> None:
        # Rumble for 0.5 seconds at 50% on each side
        if self.__controller.has_rumble:
            self.__controller.set_rumble(0.5, 0.5, 0.5)

    def LED(self, mode:int) -> None:
        if self.__controller.has_led:
            self.__controller.set_led(mode)
            time.sleep(1)

    # Button Press Functions
    def __start_button_pressed(self, button):
        pass

    def __mode_button_pressed(self, button):
        pass

    def __select_button_pressed(self, button):
        pass

    def __A_button_pressed(self, button):
        self.LED(control.LED_MODE.ROTATE_TWO)

    def __B_button_pressed(self, button):
        pass

    def __X_button_pressed(self, button):
        pass

    def __Y_button_pressed(self, button):
        pass

    def __L_trigger_pressed(self, button):
        pass

    def __R_trigger_pressed(self, button):
        pass

    def __L_shoulder_pressed(self, button):
        pass

    def __R_shoulder_pressed(self, button):
        pass

    # Button Release Functions
    def __start_button_released(self, button):
        pass

    def __mode_button_released(self, button):
        pass

    def __select_button_released(self, button):
        pass

    def __A_button_released(self, button):
        pass

    def __B_button_released(self, button):
        pass

    def __X_button_released(self, button):
        pass

    def __Y_button_released(self, button):
        pass

    def __L_trigger_released(self, button):
        pass

    def __R_trigger_released(self, button):
        pass

    def __L_shoulder_released(self, button):
        pass

    def __R_shoulder_released(self, button):
        pass

    # Axis Move Function
    def __axis_moved(self, axis):
        pass