# Dataset Suggestions for AI Waste Classifier

To train a robust CNN or TFLite model, you need a diverse dataset of waste images. Here are the top suggestions:

## 1. Public Datasets (Recommended)
- **Waste Classification Dataset (Kaggle)**: Contains ~22,000 images divided into Organic and Recyclable. [Kaggle Link](https://www.kaggle.com/datasets/techsavyy/waste-classification-data)
- **Garbage Classification (Kaggle)**: 6 classes (glass, paper, cardboard, plastic, metal, trash). Perfect for multi-class classification. [Kaggle Link](https://www.kaggle.com/datasets/asdasdasasdas/garbage-classification)
- **TACO (Trash Annotations in Context)**: Professional-grade dataset with coco-style annotations for waste in the wild. [TACO Dataset](http://tacodataset.org/)

## 2. Custom Data Collection
For a prototype, it's often best to supplement public data with images from your specific hardware setup:
- **Angle**: Capture images from the exact mounting point of your RPi Camera.
- **Lighting**: Train with images under the same lighting conditions as your final bin location.
- **Background**: Ensure the "tray" or background where waste is placed is consistent (e.g., solid white or black).

## 3. Training Tips
- **Transfer Learning**: Use a pre-trained model like **MobileNetV2** as a base. It is lightweight and fast on Raspberry Pi.
- **Data Augmentation**: Use rotations, flips, and brightness adjustments to make the model more robust.
- **TFLite Conversion**: Always convert your model to `.tflite` format and use **int8 quantization** for maximum performance on the Pi.
