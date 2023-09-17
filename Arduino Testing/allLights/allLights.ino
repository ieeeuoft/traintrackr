#include <Wire.h>
#include <Adafruit_GFX.h>
#include "Adafruit_LEDBackpack.h"

#ifndef _BV
  #define _BV(bit) (1<<(bit))
#endif


Adafruit_LEDBackpack matrix = Adafruit_LEDBackpack();

uint8_t counter = 0;
uint16_t delayTime = 500;

void setup() {
  Serial.begin(9600);  
  matrix.begin(0x70);  // pass in the address

  pinMode(3, OUTPUT);   //digital pin 3 = MCU STATUS
  analogWrite(3, 20);
}

void loop() {
    for (uint8_t c=0; c<8; c++){
        for (uint8_t a=0; a<16; a++){
            matrix.displaybuffer[c] = (1<<a);
            matrix.writeDisplay();
            delay(delayTime);
            matrix.displaybuffer[c] = 0;
        }
    }
}
