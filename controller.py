import time

try:
    import RPi.GPIO as GPIO
except ImportError:
    class MockGPIO:
        BCM = 'BCM'
        OUT = 'OUT'
        def setmode(self, mode): pass
        def setup(self, pin, mode): pass
        def output(self, pin, val): pass
        def cleanup(self): pass
        class PWM:
            def __init__(self, pin, freq): pass
            def start(self, duty): pass
            def ChangeDutyCycle(self, duty): pass
            def stop(self): pass
    GPIO = MockGPIO()
    print("WARNING: RPi.GPIO not found. Using Mock GPIO for Servo.")

class BinController:
    def __init__(self):
        # Category -> GPIO Pin mapping
        self.pins = {
            'Plastic': 17,
            'Metal': 27,
            'Paper': 22,
            'Organic': 10
        }
        GPIO.setmode(GPIO.BCM)
        self.servos = {}
        
        for cat, pin in self.pins.items():
            GPIO.setup(pin, GPIO.OUT)
            pwm = GPIO.PWM(pin, 50) # 50Hz frequency
            pwm.start(0)
            self.servos[cat] = pwm

    def open_bin(self, category):
        if category in self.servos:
            print(f"Opening {category} bin...")
            # 7.5 is 90 degrees (Middle), adjust for your servo (2.5 to 12.5)
            self.servos[category].ChangeDutyCycle(7.5) 
            time.sleep(3)
            self.servos[category].ChangeDutyCycle(2.5) # Reset to 0 degrees (Closed)
            time.sleep(1)
            self.servos[category].ChangeDutyCycle(0) # Stop pulse to prevent jitter
            print(f"{category} bin closed.")
        else:
            print(f"Error: Category {category} not recognized.")

    def cleanup(self):
        for pwm in self.servos.values():
            pwm.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    controller = BinController()
    try:
        controller.open_bin('Plastic')
        time.sleep(2)
        controller.open_bin('Organic')
    except KeyboardInterrupt:
        controller.cleanup()
