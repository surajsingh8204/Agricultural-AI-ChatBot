# 🌽 Plant Disease Detection Model

A Convolutional Neural Network (CNN) model for detecting diseases in corn/maize plants using deep learning.

## 📋 Overview

This model can identify common corn diseases and healthy plants from leaf images, helping farmers quickly diagnose crop health issues.

## 🎯 Supported Diseases

The model can classify corn plants into 4 categories:

1. **Cercospora Leaf Spot / Gray Leaf Spot**
   - Gray to tan rectangular lesions on leaves
   - Can significantly reduce yield if untreated

2. **Common Rust**
   - Circular to elongate brown pustules on leaves
   - Common in humid conditions

3. **Northern Leaf Blight**
   - Long cigar-shaped gray-green lesions
   - Major disease affecting corn worldwide

4. **Healthy**
   - No visible disease symptoms
   - Normal plant condition

## 📊 Dataset

### PlantVillage Dataset

This model is trained using the **PlantVillage Dataset**, a world-class collection of plant disease images.

**Citation:**
```
Hughes, D. P., & Salathé, M. (2015). 
An open access repository of images on plant health to enable the development of mobile disease diagnostics. 
arXiv preprint arXiv:1511.08060.
```

**Dataset Details:**
- **Source**: [PlantVillage Dataset GitHub](https://github.com/spMohanty/PlantVillage-Dataset)
- **License**: Creative Commons - Check original repository
- **Crop**: Corn (Maize)
- **Classes**: 4 (3 diseases + healthy)
- **Image Format**: RGB images of corn leaves
- **Collection**: Laboratory-controlled conditions with clean backgrounds

**Acknowledgment:**
We extend our sincere gratitude to the PlantVillage team, David P. Hughes, and Marcel Salathé for creating and maintaining this invaluable public dataset that enables AI-driven plant disease detection research.

## 🏗️ Model Architecture

### CNN Architecture
- **Framework**: TensorFlow/Keras
- **Input Shape**: RGB images (resized to model requirements)
- **Architecture**: Custom CNN with multiple convolutional layers
- **Output**: 4-class classification

### Model Files

The trained model is available in multiple formats:

```
models3/
├── 4.h5          # Keras H5 format (legacy)
├── 4.keras       # Keras format (recommended)
└── 4/            # TensorFlow SavedModel format
    ├── saved_model.pb
    ├── keras_metadata.pb
    ├── assets/
    └── variables/
        ├── variables.data-00000-of-00001
        └── variables.index
```

**Recommended Format**: Use `4.keras` for latest Keras compatibility or the `4/` folder for TensorFlow Serving.

## 📓 Training Notebook

The `training3.ipynb` notebook contains:
- Data preprocessing and augmentation
- Model architecture definition
- Training process with validation
- Performance evaluation
- Model saving in multiple formats

### Requirements

```bash
pip install tensorflow numpy pandas matplotlib opencv-python pillow
```

### Usage

```python
# Load the model
from tensorflow import keras

# Option 1: Load .keras format (recommended)
model = keras.models.load_model('models3/4.keras')

# Option 2: Load .h5 format
model = keras.models.load_model('models3/4.h5')

# Option 3: Load SavedModel format
model = keras.models.load_model('models3/4')

# Make predictions
import numpy as np
from PIL import Image

# Load and preprocess image
img = Image.open('path/to/corn_leaf.jpg')
img = img.resize((256, 256))  # Adjust size to match training
img_array = np.array(img) / 255.0
img_array = np.expand_dims(img_array, axis=0)

# Predict
predictions = model.predict(img_array)
class_names = [
    'Cercospora Leaf Spot / Gray Leaf Spot',
    'Common Rust',
    'Healthy',
    'Northern Leaf Blight'
]
predicted_class = class_names[np.argmax(predictions)]
confidence = np.max(predictions) * 100

print(f"Prediction: {predicted_class}")
print(f"Confidence: {confidence:.2f}%")
```

## 📈 Model Performance

- **Training Dataset**: PlantVillage corn subset
- **Validation Strategy**: Train-test split
- **Classes Balanced**: Yes (dataset contains balanced samples)

*(Add specific accuracy, loss, and validation metrics after training)*

## 🚀 Future Improvements

- [ ] Add more corn disease types
- [ ] Include field condition images (not just lab images)
- [ ] Implement disease severity grading
- [ ] Add real-time prediction API
- [ ] Support for multiple crop types
- [ ] Mobile app integration
- [ ] Treatment recommendations

## 🔧 Troubleshooting

### Common Issues

**1. Model loading errors**
```python
# If you get version mismatch errors, try:
import tensorflow as tf
print(tf.__version__)  # Check your TensorFlow version
```

**2. Image preprocessing**
- Ensure images are RGB (3 channels)
- Resize to the same dimensions used in training
- Normalize pixel values (0-1 range)

**3. Large model files**
- Model files are large (100+ MB)
- Use Git LFS for version control
- Or download separately from releases

## 📝 Notes

- This model is trained on laboratory images with clean backgrounds
- Real-world performance may vary with field images
- Always verify predictions with agricultural experts
- Use as a screening tool, not as the sole diagnostic method

## 🙏 Credits

- **Dataset**: PlantVillage (Hughes & Salathé, 2015)
- **Framework**: TensorFlow/Keras
- **Training**: Custom implementation

## 📄 License

This model and code are for educational and research purposes. Please cite the PlantVillage dataset when using this model.

---

**Part of the [Agricultural AI ChatBot](../README.md) project**

Last Updated: October 23, 2025
