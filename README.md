# IoT AI Waste Segregation System

This prototype uses a Raspberry Pi to automatically detect and sort waste into Plastic, Metal, Paper, and Organic bins.

## Features
- Real-time detection using HC-SR04 Ultrasonic sensor.
- AI classification using TensorFlow Lite and Raspberry Pi Camera.
- Automated bin lid control via 4 Servo motors.
- Live web dashboard to monitor classification results.

## Project Structure
- `src/main.py`: Main orchestrator script.
- `src/detector.py`: Ultrasonic sensor logic.
- `src/capture.py`: Camera interface.
- `src/classifier.py`: TFLite inference logic.
- `src/controller.py`: Servo motor control logic.
- `src/dashboard.py`: Flask-based web dashboard.
- `docs/`: Architecture diagrams and circuit guides.

## Setup Instructions

### 1. Hardware Connections
Follow the wiring diagram in `docs/circuit.md`. Ensure you use an external 5V power source for the servo motors.

### 2. Software Installation
Run the following on your Raspberry Pi:
```bash
# Update and install system dependencies
sudo apt-get update
sudo apt-get install libatlas-base-dev libopencv-dev

# Clone/Copy এই project files to /home/pi/waste_segregator
cd /home/pi/waste_segregator

# Install Python requirements
pip3 install -r requirements.txt
```

### 3. Model Preparation
- Place your trained TFLite model in `src/models/waste_classifier.tflite`.
- If no model is found, the system will run in **Demo/Mock mode** for testing.

### 4. Running the Professional Dashboard (Vite + React)
This is the recommended software dashboard for advanced analytics.

Terminal 1 (AI Logic):
```bash
python3 src/main.py
```

Terminal 2 (API Service):
```bash
python3 src/api.py
```

Terminal 3 (React Frontend):
```bash
cd dashboard
npm install
npm run dev
```
Access the professional dashboard at `http://<pi-ip-address>:5173`.

### 5. Running the Legacy Dashboard (Flask)
If you prefer a simpler, single-service dashboard:
```bash
python3 src/dashboard.py
```
Access at `http://<pi-ip-address>:5000`.

## License
MIT
