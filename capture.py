import cv2
import os
import time

class WasteCamera:
    def __init__(self, output_dir="captured_images"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Initialize camera
        # On Pi, this usually uses the legacy stack or libcamera
        # Using index 0 for standard USB or Pi Cam (with V4L2)
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def capture(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to capture image")
            return None
        
        filename = f"waste_{int(time.time())}.jpg"
        filepath = os.path.join(self.output_dir, filename)
        cv2.imwrite(filepath, frame)
        print(f"Image saved to {filepath}")
        return filepath

    def release(self):
        self.cap.release()

if __name__ == "__main__":
    cam = WasteCamera()
    cam.capture()
    cam.release()
