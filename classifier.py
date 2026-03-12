import numpy as np
import cv2
import os

try:
    # Try importing tflite-runtime (common on RPi) or full tensorflow
    try:
        from tflite_runtime.interpreter import Interpreter
    except ImportError:
        import tensorflow as tf
        Interpreter = tf.lite.Interpreter
except ImportError:
    # Generic Mock for development
    class Interpreter:
        def __init__(self, model_path): pass
        def allocate_tensors(self): pass
        def get_input_details(self): return [{"index": 0, "shape": [1, 224, 224, 3]}]
        def get_output_details(self): return [{"index": 0}]
        def set_tensor(self, index, data): pass
        def invoke(self): pass
        def get_tensor(self, index): return np.random.rand(1, 4)
    print("WARNING: TensorFlow/TFLite not found. Using Mock Classifier.")

class WasteClassifier:
    def __init__(self, model_path="models/waste_classifier.tflite"):
        self.labels = ['Plastic', 'Metal', 'Paper', 'Organic']
        self.model_path = model_path
        
        # Check if model exists, if not use mock behavior
        if not os.path.exists(model_path):
            print(f"Warning: Model file not found at {model_path}. Using Mock Inference.")
            self.mock = True
        else:
            self.mock = False
            self.interpreter = Interpreter(model_path=model_path)
            self.interpreter.allocate_tensors()
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()

    def classify(self, image_path):
        if self.mock:
            # Randomly pick a category for demonstration
            import random
            return random.choice(self.labels), 0.95

        # Load and preprocess image
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Assuming model input is 224x224
        image = cv2.resize(image, (224, 224))
        input_data = np.expand_dims(image, axis=0).astype(np.float32)
        # Normalize if required (usually /255)
        input_data = input_data / 255.0

        # Run inference
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
        
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
        prediction_idx = np.argmax(output_data)
        confidence = output_data[prediction_idx]
        
        return self.labels[prediction_idx], confidence
