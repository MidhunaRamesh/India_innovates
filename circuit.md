# Circuit Connection Guide

## Components Pinout

### 1. Ultrasonic Sensor (HC-SR04)
Connect the ultrasonic sensor to the Raspberry Pi GPIO pins:
- **VCC**: 5V (Pin 2 or 4)
- **GND**: Ground (Pin 6 or 9)
- **TRIG**: GPIO 23 (Pin 16)
- **ECHO**: GPIO 24 (Pin 18)  
  *Note: Use a voltage divider (1kΩ and 2kΩ resistors) for the ECHO pin since RPi GPIO is 3.3V.*

### 2. Servo Motors (4x)
All servos share VCC and GND. Control pins are as follows:
- **Common VCC**: External 5V 2A power supply (Do NOT power from Pi directly for 4 servos)
- **Common GND**: Ground (Must be shared with Pi Ground)
- **Servo 1 (Plastic)**: GPIO 17 (Pin 11)
- **Servo 2 (Metal)**: GPIO 27 (Pin 13)
- **Servo 3 (Paper)**: GPIO 22 (Pin 15)
- **Servo 4 (Organic)**: GPIO 10 (Pin 19)

### 3. Raspberry Pi Camera
- Connect to the **CSI port** using the ribbon cable.

## Wiring Checklist
1. Connect external 5V power supply to the Servo VCC/GND rails.
2. Connect Pi Ground to the Breadboard/Common Ground.
3. Wire the Ultrasonic sensor with the voltage divider onto the Echo line.
4. Connect all trigger/signal wires to the respective GPIO pins.
