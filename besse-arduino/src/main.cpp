#include <Arduino.h>
#include <XBOXRECV.h>
#include <controllerEnums.h>
#include <Servo.h>
#include <FastLED.h>

USB Usb;
XBOXRECV Xbox(&Usb);

Servo lMotor;
Servo rMotor;

bool ROBOT_ENABLED = false;
#define NUM_LEDS 11
#define LED_PIN 4

CRGB leds[NUM_LEDS];


// Documentation:
// https://github.com/felis/USB_Host_Shield_2.0/blob/master/examples/Xbox/XBOXRECV/XBOXRECV.ino
// https://content.vexrobotics.com/docs/217-3367-VEXpro_Jaguar_Datasheet.pdf

void setup() {
    // Start debug serial comms
    Serial.begin(115200);

    // Attach Motor Controllers
    lMotor.attach(2);
    rMotor.attach(3);

    // Check if USB initilialized successfully
    if (Usb.Init() == -1){
        Serial.println("OSC did not start!");
        while(1);
    }

    // Initialize LEDS
    FastLED.addLeds<NEOPIXEL, LED_PIN>(leds, NUM_LEDS);

    Serial.println("Xbox receiver initialized!");
    Serial.println(Xbox.getBatteryLevel());

    // Reset LEDs
    for (uint8_t i = 0; i < NUM_LEDS; i++){
        leds[i] = CRGB::Black;
    }

    FastLED.show();
}

void loop() {
    // Variables
    int16_t deadZone = 5000;
    uint8_t hue = 1;


    // Run USB comm tasks
    Usb.Task();

    // Check if the receiver is connected
    if (Xbox.XboxReceiverConnected){

        // Check if the controller is connected
        if (Xbox.Xbox360Connected[0]){

            // Enter command mode (Left and Right Triggers)
            if (Xbox.getButtonPress(L2) && Xbox.getButtonPress(R2)){

                // Enable Robot (Start)
                if (Xbox.getButtonClick(START) && !(ROBOT_ENABLED)){
                    ROBOT_ENABLED = true;
                    Xbox.setLedMode(ALTERNATING);
                    Xbox.setRumbleOn(255, 255);
                    delay(250);
                    Xbox.setRumbleOn(0, 0);
                    Xbox.setLedOn(LED1);
                    Serial.println("Enabled");
                    fill_rainbow(leds, NUM_LEDS, hue, 7);

                    
                }

                // Disable Robot (Select)
                if (Xbox.getButtonClick(SELECT) && ROBOT_ENABLED){
                    ROBOT_ENABLED = false;

                    lMotor.write(90);
                    rMotor.write(90);

                    Xbox.setLedMode(ALTERNATING);
                    Xbox.setRumbleOn(255, 255);
                    delay(250);
                    Xbox.setRumbleOn(0, 0);
                    Xbox.setLedOn(LED1);
                    Serial.println("Disabled");

                    // Reset LEDs
                    for (uint8_t i = 0; i < NUM_LEDS; i++){
                        leds[i] = CRGB::Gold;
                    }
                    
                }



            }

            // Get Joystick Values
            int32_t lMotorSpeed = Xbox.getAnalogHat(LeftHatY);
            int32_t rMotorSpeed = Xbox.getAnalogHat(RightHatY);

            // Subtract deadzone
            if (abs(lMotorSpeed) < deadZone) lMotorSpeed = 0;
            if (abs(rMotorSpeed) < deadZone) rMotorSpeed = 0;
            
            if ((lMotorSpeed || rMotorSpeed) && ROBOT_ENABLED){

                // Remap 16-bit values to servo values
                lMotorSpeed = map(lMotorSpeed, -32768, 32767, 0, 180);
                rMotorSpeed = map(rMotorSpeed, -32768, 32767, 0, 180);

            }
            else {
                // Remap 16-bit values to servo values
                lMotorSpeed = map(0, -32768, 32767, 0, 180);
                rMotorSpeed = map(0, -32768, 32767, 0, 180);
            }


            // Serial.println("-----------");
            // Serial.println(lMotorSpeed);
            // Serial.println(rMotorSpeed);

            // Drive motors with PWM 
                lMotor.write(lMotorSpeed);
                rMotor.write(rMotorSpeed);

            FastLED.show();
            FastLED.delay(1000/60); 

        }
        else {
            uint8_t lMotorSpeed = map(0, -32768, 32767, 0, 180);
            uint8_t rMotorSpeed = map(0, -32768, 32767, 0, 180);

            lMotor.write(lMotorSpeed);
            rMotor.write(rMotorSpeed);
        }




    }

}