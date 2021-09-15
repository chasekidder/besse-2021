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

import modules.control as control
import modules.drive as drive
import modules.effects as effects

import time

def remap(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def main():
    loop = True
    start = time.time()
    ctrl = control.controller()
    robot = drive.DriveTrain()

    while loop:
        if time.time() >= start + (60 * 5):
            print("5 minutes elapsed. Ending program...")
            loop = False
        
        else:
            ctrl.get_buttons()
            
            if ctrl.buttons["ABS_Y"] != 0 or ctrl.buttons["ABS_RY"] != 0:
                l_ratio = remap(ctrl.buttons["ABS_Y"], -32768, 32768, -1, 1) 
                r_ratio = remap(ctrl.buttons["ABS_RY"], -32768, 32768, -1, 1) 
    
                robot.drive(l_ratio, r_ratio)




if __name__ == "__main__":
    main()