import gpiozero as gpio
from gpiozero.pins.pigpio import PiGPIOFactory

LF_MOTOR_PIN = 17
LR_MOTOR_PIN = 18
RF_MOTOR_PIN = 19
RR_MOTOR_PIN = 20

class JAGUAR_PWM:
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

    def drive(self, speed:float, reverseDirection:bool=False) -> None:
        if speed <= 1 and speed >= -1:
            self.__drive_motor(speed * int(reverseDirection))
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
        
        self.LF_motor = Motor(LF_MOTOR_PIN)
        self.LR_motor = Motor(LR_MOTOR_PIN)
        self.RF_motor = Motor(RF_MOTOR_PIN)
        self.RR_motor = Motor(RR_MOTOR_PIN)
    
    def drive(self, speed_L:float, speed_R:float,reverseDirectionL:bool=False, reverseDirectionR:bool=False) -> None:
        # TODO: Find out which motors are reversed and refactor the inversion here
        if speed_L <= 1 and speed_L >= -1 and speed_R <= 1 and speed_R >= -1:
            self.LF_motor.drive(-1 * speed_L * int(reverseDirectionL))
            self.LR_motor.drive(-1 * speed_L * int(reverseDirectionL))

            self.RF_motor.drive(speed_R * int(reverseDirectionR))
            self.RR_motor.drive(speed_R * int(reverseDirectionR))

        else:
            self.LF_motor.E_STOP = True
            self.LR_motor.E_STOP = True
            self.RF_motor.E_STOP = True
            self.RR_motor.E_STOP = True

            raise ValueError("Motors can not be given a value outside of -1 to +1.")
        