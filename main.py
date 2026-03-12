import time
import os
from detector import UltrasonicDetector
from capture import WasteCamera
from classifier import WasteClassifier
from controller import BinController

# Global state for dashboard
STATE_FILE = "system_state.json"

def update_state(category, confidence):
    state = {
        "last_detected": {
            "category": category,
            "confidence": f"{confidence*100:.1f}%",
            "timestamp": time.strftime("%H:%M:%S")
        },
        "stats": {
            "Plastic": 0, "Metal": 0, "Paper": 0, "Organic": 0
        },
        "history": []
    }
    
    # Load existing state if it exists
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                state = json.load(f)
        except:
            pass

    # Update last detected
    state["last_detected"] = {
        "category": category,
        "confidence": f"{confidence*100:.1f}%",
        "timestamp": time.strftime("%H:%M:%S")
    }
    
    # Update stats
    if category in state["stats"]:
        state["stats"][category] += 1
    
    # Update history (keep last 10)
    state["history"].insert(0, state["last_detected"])
    state["history"] = state["history"][:10]
    
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def main():
    print("Starting AI Waste Segregation System...")
    
    # Initialize components
    detector = UltrasonicDetector()
    camera = WasteCamera()
    classifier = WasteClassifier()
    controller = BinController()
    
    print("System Ready. Waiting for waste...")
    
    try:
        while True:
            # Step 1: Detect object
            if detector.is_triggered(threshold=15):
                print("\nWaste Detected! Initiating segregation...")
                
                # Step 2: Capture Image
                image_path = camera.capture()
                if not image_path:
                    continue
                
                # Step 3: Classify
                category, confidence = classifier.classify(image_path)
                print(f"Classification: {category} ({confidence*100:.1f}%)")
                
                # Update system state for dashboard
                update_state(category, confidence)

                # Step 4: Actuate Servo
                controller.open_bin(category)
                
                # Wait before next detection to avoid double triggers
                time.sleep(2)
                print("Waiting for next object...")
            
            time.sleep(0.5) # Polling rate
            
    except KeyboardInterrupt:
        print("\nStopping system...")
    finally:
        controller.cleanup()
        camera.release()

if __name__ == "__main__":
    main()
