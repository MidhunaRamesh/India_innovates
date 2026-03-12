import time

try:
    import RPi.GPIO as GPIO
except ImportError:
    # Mock GPIO for non-Raspberry Pi environments
    class MockGPIO:
        BCM = 'BCM'
        OUT = 'OUT'
        IN = 'IN'
        HIGH = 1
        LOW = 0
        def setmode(self, mode): pass
        def setup(self, pin, mode): pass
        def output(self, pin, val): pass
        def input(self, pin): return 0
        def cleanup(self): pass
    GPIO = MockGPIO()
    print("WARNING: RPi.GPIO not found. Using Mock GPIO.")

class UltrasonicDetector:
    def __init__(self, trig_pin=23, echo_pin=24):
        self.trig = trig_pin
        self.echo = echo_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

    def get_distance(self):
        # Trigger the pulse
        GPIO.output(self.trig, GPIO.LOW)
        time.sleep(0.000002)
        GPIO.output(self.trig, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.trig, GPIO.LOW)

        # Measure time for echo
        start_time = time.time()
        stop_time = time.time()

        while GPIO.input(self.echo) == 0:
            start_time = time.time()
        
        while GPIO.input(self.echo) == 1:
            stop_time = time.time()

        elapsed = stop_time - start_time
        # Distance = (time * speed of sound) / 2
        distance = (elapsed * 34300) / 2
        return distance

    def is_triggered(self, threshold=10):
        dist = self.get_distance()
        return dist < threshold

if __name__ == "__main__":
    detector = UltrasonicDetector()
    try:
        while True:
            dist = detector.get_distance()
            print(f"Distance: {dist:.1f} cm")
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
