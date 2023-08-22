#include <Wire.h>
#include <Adafruit_GFX.h>
#include "Adafruit_LEDBackpack.h"

#ifndef _BV
  #define _BV(bit) (1<<(bit))
#endif


Adafruit_LEDBackpack matrix = Adafruit_LEDBackpack();

uint8_t counter = 0;
uint16_t delayTime = 200;

void setup() {
  Serial.begin(9600);
  Serial.println("another test");
  
  matrix.begin(0x70);  // pass in the address
}

void loop() {
    for (uint8_t i = 0; i < 4; i++){
        matrix.displaybuffer[i] = 0b111111;
    }

    matrix.writeDisplay();
    delay(1000);

    for (uint8_t i = 0; i < 4; i++){
        matrix.displaybuffer[i] = 0;
    }

    matrix.writeDisplay();
    delay(1000);
}
