#include <stdio.h>
#include <stdint.h>


int main(){
    uint16_t displaybuffer[8];

    for (uint8_t counter = 0; counter < 16; counter++){
        for (uint8_t i=0; i <8; i++){
            displaybuffer[i] = (1 << ((counter + i) % 16)) | (1 << ((counter + i + 8) % 16));
            printf("%d\n", displaybuffer[i]); 
        }
        printf("-------------");
    }
    return 0;
}

