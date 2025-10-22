# 🌾 Agricultural AI ChatBot

An intelligent AI-powered chatbot system designed to assist farmers and agricultural professionals with disease detection, animal species identification, and agricultural guidance using deep learning and large language models.

## 🎯 Project Overview

This comprehensive agricultural AI platform combines multiple AI technologies to provide:
- Real-time plant disease detection
- Animal species identification
- Natural language conversation with fine-tuned agricultural LLM
- Expert agricultural advice and recommendations

## 📁 Project Structure

```
Agricultural-AI-ChatBot/
├── disease-detection-model/          # Plant disease detection using CNN
│   ├── training3.ipynb               # Training notebook
│   ├── models3/                      # Trained models
│   └── PlantVillage3/                # Training dataset
│
├── animalspecies-detection-model/    # Animal species identification (Coming Soon)
│
├── fine-tuned-llm-model/             # Fine-tuned LLM for agriculture (Coming in 1-2 days)
│
├── chatbot-backend/                   # Backend API (Future)
│
└── chatbot-frontend/                  # User interface (Future)
```

## 🚀 Current Features

### ✅ Plant Disease Detection
- **Status**: Operational
- **Technology**: Convolutional Neural Network (CNN)
- **Dataset**: PlantVillage Dataset
- **Supported Crops**: Corn/Maize
- **Diseases Detected**:
  - Cercospora Leaf Spot / Gray Leaf Spot
  - Common Rust
  - Northern Leaf Blight
  - Healthy Plant Detection

### 🔄 In Progress

#### Fine-Tuned Agricultural LLM
- **Status**: In Development (Expected: 1-2 days)
- **Purpose**: Natural language understanding for agricultural queries
- **Capabilities**: Crop advice, disease information, farming best practices

#### Animal Species Detection
- **Status**: Planned
- **Purpose**: Identify livestock and farm animals

## 🛠️ Technologies Used

- **Deep Learning**: TensorFlow/Keras, PyTorch
- **Computer Vision**: OpenCV, CNN architectures
- **NLP**: Large Language Models (LLM)
- **Backend**: Python (FastAPI/Flask - planned)
- **Frontend**: React/Streamlit (planned)

## 📊 Dataset Attribution

### PlantVillage Dataset
The plant disease detection model is trained on the **PlantVillage Dataset**:

- **Citation**: Hughes, D. P., & Salathé, M. (2015). An open access repository of images on plant health to enable the development of mobile disease diagnostics. *arXiv preprint arXiv:1511.08060*.
- **Source**: [PlantVillage Dataset](https://github.com/spMohanty/PlantVillage-Dataset)
- **License**: Creative Commons (Check original repository for specific license)
- **Description**: A comprehensive database of plant leaf images covering multiple crops and diseases

**We are grateful to the PlantVillage team for making this valuable dataset publicly available for research and development.**

## 🎓 Model Performance

### Disease Detection Model
- **Architecture**: Custom CNN
- **Training Dataset**: PlantVillage (Corn subset)
- **Classes**: 4 (3 diseases + healthy)
- **Model Format**: Keras (.h5, .keras) and SavedModel

## 🔮 Future Roadmap

- [ ] Complete fine-tuned agricultural LLM integration
- [ ] Implement animal species detection model
- [ ] Develop RESTful API backend
- [ ] Create user-friendly web interface
- [ ] Add mobile app support
- [ ] Integrate weather data and crop recommendations
- [ ] Multi-language support
- [ ] Real-time disease severity assessment
- [ ] Treatment recommendations with local availability
- [ ] Community forum for farmers

## 💻 Installation & Usage

### Disease Detection Model

```bash
# Navigate to disease detection folder
cd disease-detection-model

# Install dependencies
pip install tensorflow numpy pandas matplotlib opencv-python

# Open the training notebook
jupyter notebook training3.ipynb
```

### Fine-Tuned LLM (Coming Soon)
Instructions will be added once the model is ready.

## 📝 Development Timeline

- **Phase 1**: Plant Disease Detection ✅ **COMPLETE**
- **Phase 2**: Fine-Tuned Agricultural LLM 🔄 **IN PROGRESS** (1-2 days)
- **Phase 3**: Animal Species Detection 📅 **PLANNED**
- **Phase 4**: Backend API Development 📅 **PLANNED**
- **Phase 5**: Frontend Development 📅 **PLANNED**
- **Phase 6**: Integration & Deployment 📅 **PLANNED**

## 🤝 Contributing

This is an active development project. Contributions, suggestions, and feedback are welcome!

## 📄 License

This project is under development. License details will be added soon.

## 👨‍💻 Author

**Suraj**
- Building an AI-powered solution for smart agriculture
- Combining computer vision and NLP for farmer assistance

## 🙏 Acknowledgments

- **PlantVillage** team for the disease detection dataset
- Open-source community for TensorFlow, Keras, and other tools
- Agricultural experts and farmers who inspire this work

## 📧 Contact

For questions, suggestions, or collaboration opportunities, please open an issue or reach out!

---

**Note**: This project is under active development. Features and documentation will be updated regularly.

Last Updated: October 23, 2025
