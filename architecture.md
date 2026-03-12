# IoT AI Waste Segregation System Architecture

## Overview
The system is designed to automate waste segregation using Computer Vision and IoT. It uses an Ultrasonic sensor to trigger the classification process and Servo motors to route waste into specific bins.

## System Flow
1. **Detection**: Ultrasonic sensor constantly monitors for objects. When an object is within 10cm, a trigger is sent.
2. **Capture**: The Raspberry Pi Camera captures a high-resolution image of the object.
3. **Classification**: 
    - The image is preprocessed (resized, normalized).
    - A TensorFlow Lite model processes the image.
    - Result categories: `Plastic`, `Metal`, `Paper`, `Organic`.
4. **Segregation**: 
    - The Pi identifies the category.
    - It sends a PWM signal to the corresponding Servo motor (Servo 1 for Plastic, 2 for Metal, etc.).
    - The servo opens the bin for 3 seconds and then closes.
5. **Monitoring**: A Flask dashboard displays the last detected item and real-time status.

## Data Flow Diagram
[Ultrasonic Sensor] -> (Distance < 10cm) -> [RPi GPIO]
[RPi GPIO] -> [Camera Capture] -> [Image File]
[Image File] -> [TFLite Model] -> [Category Label]
[Category Label] -> [RPi GPIO] -> [Servo Motor X]
[Category Label] -> [Flask Dashboard]
