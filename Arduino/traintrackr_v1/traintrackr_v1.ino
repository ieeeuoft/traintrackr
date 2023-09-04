#include <Wire.h>
#include <Adafruit_GFX.h>
#include "Adafruit_LEDBackpack.h"

#ifndef _BV
  #define _BV(bit) (1<<(bit))
#endif


Adafruit_LEDBackpack matrix = Adafruit_LEDBackpack();

uint8_t counter = 0;
uint16_t delayTime = 200;
int firstTimer = 0;

void setup() {
  Serial.begin(9600);
  Serial.println("another test");
  
  matrix.begin(0x70);  // pass in the address
}

void loop() {
  // matrix.displaybuffer[3] = (1<<0);
  // squarebracket = row (C), leftshift = col (A)

  // String received = "A00C1A00C2A00C3A00C0A01C0"; for testing
 
  
  if (Serial.available() > 0) {
    String received = Serial.readStringUntil('\n');
    int a;
    int c;

    int upper_limit = received.length() / 5;
    for (int i = 0; i < upper_limit; i++){
      a = (received[i * 5 + 1] - 48) * 10 + (received[i * 5 + 2] - 48);
      c = received[i * 5 + 4] - 48;
      matrix.displaybuffer[c] = (1 << a);
    }
    matrix.writeDisplay();
    Serial.println("Received and Board Lit");
    Serial.flush();
  }
}
