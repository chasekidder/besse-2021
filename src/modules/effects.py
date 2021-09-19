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

# modules/effects.py

import threading
import time
from rpi_ws281x import Color, PixelStrip, ws

# LED strip configuration:
LED_COUNT = 10        # Number of LED pixels.
LED_PIN = 18           # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000   # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10           # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255   # Set to 0 for darkest and 255 for brightest
LED_INVERT = False     # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0
LED_STRIP = ws.SK6812_STRIP_RGBW

class LED_Strip():
    def __init__(self):
        self.__LEDs = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
        self.__LEDs.begin()

    # Define functions which animate LEDs in various ways.
    def colorWipe(self, color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        for i in range(self.__LEDs.numPixels()):
            self.__LEDs.setPixelColor(i, color)
            self.__LEDs.show()
            time.sleep(wait_ms / 1000.0)


    def theaterChase(self, color, wait_ms=50, iterations=10):
        """Movie theater light style chaser animation."""
        for j in range(iterations):
            for q in range(3):
                for i in range(0, self.__LEDs.numPixels(), 3):
                    self.__LEDs.setPixelColor(i + q, color)
                self.__LEDs.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, self.__LEDs.numPixels(), 3):
                    self.__LEDs.setPixelColor(i + q, 0)


    def wheel(self, pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)


    def rainbow(self, wait_ms=20, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256 * iterations):
            for i in range(self.__LEDs.numPixels()):
                self.__LEDs.setPixelColor(i, self.wheel((i + j) & 255))
            self.__LEDs.show()
            time.sleep(wait_ms / 1000.0)


    def rainbowCycle(self, wait_ms=20, iterations=5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256 * iterations):
            for i in range(self.__LEDs.numPixels()):
                self.__LEDs.setPixelColor(i, self.wheel(((i * 256 // self.__LEDs.numPixels()) + j) & 255))
            self.__LEDs.show()
            time.sleep(wait_ms / 1000.0)


    def theaterChaseRainbow(self, wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
            for q in range(3):
                for i in range(0, self.__LEDs.numPixels(), 3):
                    self.__LEDs.setPixelColor(i + q, self.wheel((i + j) % 255))
                self.__LEDs.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, self.__LEDs.numPixels(), 3):
                    self.__LEDs.setPixelColor(i + q, 0)

    def demo(self):
        self.__thread = threading.Thread(target=self.threaded_demo)
        self.__thread.start()

    def threaded_demo(self):
        # Color wipe animations.
        self.colorWipe(Color(255, 0, 0))  # Red wipe
        self.colorWipe(Color(0, 255, 0))  # Blue wipe
        self.colorWipe(Color(0, 0, 255))  # Green wipe
        self.colorWipe(Color(0, 0, 0, 255))  # White wipe
        self.colorWipe(Color(255, 255, 255))  # Composite White wipe
        self.colorWipe(Color(255, 255, 255, 255))  # Composite White + White LED wipe

        # Theater chase animations.
        self.theaterChase(Color(127, 0, 0))  # Red theater chase
        self.theaterChase(Color(0, 127, 0))  # Green theater chase
        self.theaterChase(Color(0, 0, 127))  # Blue theater chase
        self.theaterChase(Color(0, 0, 0, 127))  # White theater chase
        self.theaterChase(Color(127, 127, 127, 0))  # Composite White theater chase
        self.theaterChase(Color(127, 127, 127, 127))  # Composite White + White theater chase

        # Rainbow animations.
        self.rainbow()
        self.rainbowCycle()
        self.theaterChaseRainbow()