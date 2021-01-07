#include <Arduino.h>

#include "rgbled.hpp"

#include "BluetoothSerial.h"
// #include <SoftwareSerial.h>


BluetoothSerial SerialBT;

// SoftwareSerial serial_con_hexapod(2, 15);

RGBled led(1, 2, 3);

typedef enum {
    SLAVE,
    REMOTE_CONTROLLED,
    AUTONOMOUS,
} firmware_mode_e;
firmware_mode_e firmware_mode;

const uint8_t PIN_MODE_SELECTOR_1 = 8;
const uint8_t PIN_MODE_SELECTOR_2 = 9;

void setup()
{
    Serial.begin(115200);
    // serial_con_hexapod.begin(9600);
    SerialBT.begin("HexaPoC");

    pinMode(PIN_MODE_SELECTOR_1, INPUT_PULLDOWN);
    pinMode(PIN_MODE_SELECTOR_2, INPUT_PULLDOWN);

    const uint8_t state1 = digitalRead(PIN_MODE_SELECTOR_1);
    const uint8_t state2 = digitalRead(PIN_MODE_SELECTOR_2);

    if (state1 && !state2) {
        firmware_mode = SLAVE;
        led.setColor(RGB_RED);
    } else if (state2 && !state1) {
        firmware_mode = REMOTE_CONTROLLED;
        led.setColor(RGB_GREEN);
    } else { // !state1 && !state2
        firmware_mode = AUTONOMOUS;
        led.setColor(RGB_BLUE);
    }

    switch (firmware_mode) {
        case SLAVE:
            break;
        case REMOTE_CONTROLLED:
            break;
        case AUTONOMOUS:
            break;
    }
}
   // if (Serial.available()) {
    //     SerialBT.write(Serial.read());
    // }
    // if (SerialBT.available()) {
        // Serial.write(SerialBT.read());
    // }
    // delay(20);

void loop()
{
    // never read
}