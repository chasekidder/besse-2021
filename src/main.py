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

import modules.effects as effects

import time

def main():
    loop = True
    start = time.time()
    ctrl = control.controller()

    while loop:
        if time.time() >= start + 60:
            print("Ending program...")
            loop = False
        
        else:
            control.controller.get_keys()

    





if __name__ == "__main__":
    main()