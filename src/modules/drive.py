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

# modules/drive.py

import gpiozero as gpio
from gpiozero.pins.pigpio import PiGPIOFactory

L_MOTOR_PIN = 22
R_MOTOR_PIN = 23


class JAGUAR_PWM:
    # https://robotcombat.com/products/images/IFI-JAGUAR_datasheet.pdf
    # http://www.team358.org/files/programming/ControlSystem2015-2019/specs/217-3367-VEXpro_Jaguar_GettingStartedGuide.pdf
    # https://frc971.org/files/jaguar/2012/MDL-BDC24_BlackJaguar-FRC_2012_FAQ-spma033a.pdf
    
    FREQUENCY = 15000 # 15kHz
    FRAME_WIDTH = 20/1000 # 20ms (5.0125ms <=> 29.985ms)
    MIN_PULSE_WIDTH = 0.67/1000 # 0.67ms
    MAX_PULSE_WIDTH = 2.33/1000 # 2.33ms

class Motor():
    """ Base Motor Class """
    def __init__(self, pin:int) -> None:
        self.__motor_controller = gpio.Servo(
            pin=pin, 
            initial_value=0.00, 
            min_pulse_width=JAGUAR_PWM.MIN_PULSE_WIDTH, 
            max_pulse_width=JAGUAR_PWM.MAX_PULSE_WIDTH, 
            frame_width=JAGUAR_PWM.FRAME_WIDTH
            )

        self.E_STOP = False

    def forward(self, speed:float) -> None:
        if speed > 0 and speed < 1:
            self.__drive_motor(speed)
        else:
            print("Motor.forward(): Negative values not allowed.")

    def backward(self, speed:float) -> None:
        if speed > 0 and speed < 1:
            self.__drive_motor(speed * -1)
        else:
            self.__power = 0
            print("Motor.backward(): Negative values not allowed.")

    def drive(self, speed:float, reverseDirection:int=1) -> None:
        if speed <= 1 and speed >= -1:
            self.__drive_motor(speed * reverseDirection)
        
        else:
            self.__motor_controller.value = 0
            self.__motor_controller.detach()
            raise ValueError("Motors can not be given a value outside of -1 to +1.")

    def __drive_motor(self, power:float) -> None:
        if self.E_STOP == True:
            power = 0
            self.__motor_controller.detach()

        if power >= -1 and power <= 1 and self.E_STOP == False:
            self.__motor_controller.value = power

        else:
            self.__motor_controller.value = 0
            self.__motor_controller.detach()
            raise ValueError("Motors can not be given a value outside of -1 to +1.")

class DriveTrain():
    def __init__(self) -> None:
        # Change to pigpio pin factory for improved timing
        gpio.Device.pin_factory = PiGPIOFactory()
        
        self.L_motor = Motor(L_MOTOR_PIN)
        self.R_motor = Motor(R_MOTOR_PIN)


        self.E_STOP = False
    
    def drive(self, speed_L:float, speed_R:float,reverseDirectionL:int=1, reverseDirectionR:int=1) -> None:
        # TODO: Find out which motors are reversed and refactor the inversion here
        if speed_L <= 1 and speed_L >= -1 and speed_R <= 1 and speed_R >= -1 and self.E_STOP == False:
            self.L_motor.drive(-1 * speed_L * reverseDirectionL)
            self.R_motor.drive(speed_R * reverseDirectionR)

        else:
            self.E_STOP = True
            self.L_motor.E_STOP = True
            self.R_motor.E_STOP = True

            self.L_motor.drive(0)
            self.R_motor.drive(0)

            raise ValueError("Motors can not be given a value outside of -1 to +1.")

    def ENABLE_E_STOP(self):
        self.E_STOP = True
        self.L_motor.E_STOP = True
        self.R_motor.E_STOP = True

        self.L_motor.drive(0)
        self.R_motor.drive(0)
