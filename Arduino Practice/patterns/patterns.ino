#include <Wire.h>
#include <Adafruit_GFX.h>
#include "Adafruit_LEDBackpack.h"

#ifndef _BV
  #define _BV(bit) (1<<(bit))
#endif


Adafruit_LEDBackpack matrix = Adafruit_LEDBackpack();

uint8_t counter = 0;
uint16_t delayTime = 100;

void setup() {
  Serial.begin(9600);
  Serial.println("another test");
  
  matrix.begin(0x70);  // pass in the address
}

void loop() {
    //go row by row
    // for (uint8_t i=0; i<4; i++) {
    
    //     matrix.displaybuffer[i] = 0b111111;
    //     matrix.writeDisplay();
    //     delay(delayTime);
    //     matrix.displaybuffer[i] = 0;
    // }
    
    // how to "switch" from row to column? (like how does it know)
    // how would we set up A and C (which is row and which is column)
    // is there a way to set one specific light to on (like displayBuffer[i][j])
    // matrix.displaybuffer[3] = (1<<0);
    // // squarebracket = row (C), leftshift = col (A)
    // matrix.writeDisplay();

    //go column by column
    for (uint8_t i=0; i<16; i++){
        for (uint8_t c=0; c<8; c++){
            matrix.displaybuffer[c] = (1<<i);
            matrix.writeDisplay();
            delay(delayTime);
            matrix.displaybuffer[c] = 0;
        }
    }

    // for (uint8_t c=0; c<4; c++){
    //     matrix.displaybuffer[c] = 0;
    // }

    // //go column by column
    // for (uint8_t i=0; i<6; i++){
    //     for (uint8_t c=0; c<4; c++){
    //         matrix.displaybuffer[c] = (1<<(5-i));
    //     }

    //     matrix.writeDisplay();
    //     delay(delayTime);
    // }

    // for (uint8_t c=0; c<4; c++){
    //     matrix.displaybuffer[c] = 0;
    // }

    // //go row by row (opposite)
    // for (uint8_t i=0; i<4; i++) {
    //     if (i != 3){
    //         matrix.displaybuffer[3-i] = 0b111111;
    //         matrix.writeDisplay();
    //         delay(delayTime);
    //         matrix.displaybuffer[3-i] = 0;
    //     }  
    // }
}
