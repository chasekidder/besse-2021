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

# main.py





import time
import os



def remap(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def main():
    loop = True
    ROBOT_ENABLED = False
    e_stop_counter = 0
    e_stop_timer = 0
    e_stop_timeout = 0

    leds = None
    ctrl = None
    robot = None

    start = time.time()

    # Effects Subsystem Initialization
    import modules.effects as effects
    leds = effects.LED_Strip()
    leds.demo()

    # Controller Subsystem Initialization
    while ctrl is None:
        if os.path.exists("/dev/input/js0"):
            print("Controller Found!")
            import modules.control as control
            ctrl = control.controller()
            #   The inputs library can only read the device 
            #   list once so we need to make sure our OS 
            #   is detecting the gamepad before importing.

        else:
            print("Waiting for controller...")
            time.sleep(1)

    # Drive Train Subsystem Initialization
    import modules.drive as drive
    robot = drive.DriveTrain()


    

    while loop:
        if time.time() >= start + (60 * 5):
            print("5 minutes elapsed. Ending program...")
            loop = False
        
        else:
            ctrl.get_buttons()

            # Check if Robot is Enabled
            if ROBOT_ENABLED:

                # Check for E-Stop (B button pressed 3 times)
                if e_stop_counter >= 5:
                        robot.ENABLE_E_STOP()
                        ROBOT_ENABLED = False

                # E-Stop has timed out so reset the counter
                elif time.time() >= e_stop_timeout:
                    e_stop_counter = 0
                    e_stop_timer = 0
                    e_stop_timeout = 0

                # Start the E-Stop timer and counter
                elif ctrl.buttons["BTN_EAST"] == 1 and e_stop_counter == 0:
                    e_stop_counter = e_stop_counter + 1
                   
                    # Add a 5 second timeout for the button presses
                    e_stop_timer = time.time()
                    e_stop_timeout = e_stop_timer + 5 

                # Increment the counter if button presses are detected
                elif ctrl.buttons["BTN_EAST"] == 0 and e_stop_counter == 1:
                    e_stop_counter = e_stop_counter + 1

                elif ctrl.buttons["BTN_EAST"] == 1 and e_stop_counter == 2:
                    e_stop_counter = e_stop_counter + 1

                elif ctrl.buttons["BTN_EAST"] == 0 and e_stop_counter == 3:
                    e_stop_counter = e_stop_counter + 1

                elif ctrl.buttons["BTN_EAST"] == 1 and e_stop_counter == 4:
                    e_stop_counter = e_stop_counter + 1


                # Handle Joystick Inputs
                if ctrl.buttons["ABS_Y"] != 0 or ctrl.buttons["ABS_RY"] != 0:
                    l_ratio = remap(ctrl.buttons["ABS_Y"], -32768, 32768, -1, 1) 
                    r_ratio = remap(ctrl.buttons["ABS_RY"], -32768, 32768, -1, 1) 
                    robot.drive(l_ratio, r_ratio)


            # Check Enabled Keys are Held (R and L Triggers and Start Button must be held)
            elif ctrl.buttons["ABS_RZ"] > 250 and ctrl.buttons["ABS_Z"] > 250 and ctrl.buttons["BTN_START"] == 1:
                ROBOT_ENABLED = True
                print("Robot Enabled")

            else:
                pass




if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        pass