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
    
}
