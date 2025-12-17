# 🌱 Plant Disease Detection - Multi-Crop AI Web Application

[![Live Demo](https://img.shields.io/badge/demo-live-success)](https://plant-disease-frontend-ibpp.onrender.com)
[![Backend API](https://img.shields.io/badge/API-active-blue)](https://plant-disease-api-yt7l.onrender.com)

AI-powered web application for detecting plant diseases across 10 crops using deep learning CNN models trained on TensorFlow. Deployed and accessible 24/7.

## 🌐 Live Application

- **Frontend**: [https://plant-disease-frontend.onrender.com](https://plant-disease-frontend-ibpp.onrender.com)
- **Backend API**: [https://plant-disease-api-yt7l.onrender.com](https://plant-disease-api-yt7l.onrender.com)
- **GitHub**: [https://github.com/surajsingh8204/PlantDiseaseDetection](https://github.com/surajsingh8204/PlantDiseaseDetection)

## ✨ Features

### Core Functionality
- 🌾 **10 Crop Support**: Organized in 3 categories
  - 🥔 **Vegetables**: Potato, Tomato, Bell Pepper
  - 🍎 **Fruits**: Apple, Mango, Sugarcane
  - � **Grains**: Rice, Wheat, Finger Millet, Maize
- 🖼️ **Drag & Drop Interface**: Easy-to-use image upload
- 📸 **Camera Capture**: Take photos directly from your device
- ✂️ **Image Cropping**: Crop and adjust captured images before analysis
- ⚡ **Real-time Detection**: Instant disease classification with confidence scores
- 💊 **Treatment Recommendations**: Get actionable advice for detected diseases
- � **Crop-Disease Reference**: Comprehensive list of all crops and their diseases
- �📱 **Mobile Responsive**: Fully optimized for smartphones and tablets
- 💡 **Photo Tips**: Built-in guidance for taking quality plant photos
- 🎨 **Category-Based Navigation**: Organized tabbed interface for easy crop selection

### Supported Disease Classes (50+ Total)

| Category | Crop | Disease Classes | Count |
|----------|------|----------------|-------|
| **🥔 Vegetables** | **Potato** | Early Blight, Late Blight, Healthy | 3 |
| | **Tomato** | Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Septoria Leaf Spot, Spider Mites, Target Spot, Mosaic Virus, Yellow Leaf Curl Virus, Healthy | 10 |
| | **Bell Pepper** | Bacterial Spot, Healthy | 2 |
| **🍎 Fruits** | **Apple** | Apple Scab, Black Rot, Cedar Apple Rust, Healthy | 4 |
| | **Mango** | Anthracnose, Bacterial Canker, Cutting Weevil, Die Back, Gall Midge, Powdery Mildew, Sooty Mould, Healthy | 8 |
| | **Sugarcane** | Bacterial Blight, Red Rot, Rust, Mosaic, Yellow Leaf Disease, Healthy | 6 |
| **🌾 Grains** | **Rice** | Bacterial Leaf Blight, Brown Spot, Leaf Smut, Healthy | 4 |
| | **Wheat** | Brown Rust, Yellow Rust, Healthy | 3 |
| | **Finger Millet** | Blast (Downy), Mottle, Seedling Disease, Smut, Wilt, Healthy | 6 |
| | **Maize** | Common Rust, Gray Leaf Spot, Northern Leaf Blight, Healthy | 4 |

## 🏗️ Project Structure

```
PlantDiseaseDetection/
├── models/              # Potato disease model
│   ├── 1/              # TensorFlow SavedModel
│   ├── 1.keras         # Keras format
│   └── 1.h5           # H5 format
├── models1/            # Pepper disease model
│   ├── 2/
│   ├── 2.keras
│   └── 2.h5
├── models2/            # Tomato disease model
│   ├── 3/
│   ├── 3.keras
│   └── 3.h5
├── models3/            # Maize disease model
│   ├── 4/
│   ├── 4.keras
│   └── 4.h5
├── models4/            # Apple disease model
│   ├── 5/
│   ├── 5.keras
│   └── 5.h5
├── models5/            # Wheat disease model
│   ├── 6/
│   ├── 6.keras
│   └── 6.h5
├── models6/            # Rice disease model
│   ├── 7/
│   ├── 7.keras
│   └── 7.h5
├── models7/            # Mango disease model
│   ├── 8/
│   ├── 8.keras
│   └── 8.h5
├── models8/            # Sugarcane disease model
│   ├── 9/
│   ├── 9.keras
│   └── 9.h5
├── models9/            # Finger Millet disease model
│   ├── 10/
│   ├── 10.keras
│   └── 10.h5
├── backend/
│   ├── main.py         # FastAPI backend server
│   └── requirements.txt
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js      # Main React component
│   │   ├── App.css     # Styles
│   │   ├── index.js
│   │   ├── vegi2.png   # Vegetables background
│   │   ├── fruits1.jpg # Fruits background
│   │   └── grains.jpg  # Grains background
│   └── package.json
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.13+
- Node.js 16+
- npm or yarn
- Git

### Local Development Setup

#### Backend Setup

1. **Navigate to backend directory:**
   ```powershell
   cd backend
   ```

2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Start the FastAPI server:**
   ```powershell
   python main.py
   ```
   
   Backend runs on `http://localhost:8000`

#### Frontend Setup

1. **Navigate to frontend directory:**
   ```powershell
   cd frontend
   ```

2. **Install npm dependencies:**
   ```powershell
   npm install
   ```

3. **Start the React development server:**
   ```powershell
   npm start
   ```
   
   Frontend opens at `http://localhost:3000`

## 🎯 Usage

### Web Application

1. Visit the live application or run locally
2. **Select Category**: Choose from Vegetables 🥔, Fruits 🍎, or Grains 🌾
3. **Select Crop Type**: Pick the specific crop from the selected category
4. **Upload Image**: 
   - Drag & drop an image, OR
   - Click to browse files, OR
   - Use camera to take a photo (with cropping)
5. **View Results**: 
   - Disease classification
   - Confidence percentage
   - Treatment recommendations
6. **Crop-Disease List**: Click the 📋 button (top-right) to view all supported crops and diseases

### Camera & Cropping Feature

1. Click the **📸 Take Photo** button
2. Capture image using your device camera
3. **Crop the image** in the cropping modal:
   - Drag to reposition
   - Use zoom slider to adjust size
   - Click **"✓ Apply & Analyze"** to proceed
4. Get instant disease prediction

### Photo Tips 💡

Click the tips button (💡) to see guidelines for best results:
- Good lighting, no shadows
- Clear focus on affected leaf areas
- Fill frame with leaf/plant part
- Avoid blurry or dark images
- Include both healthy and diseased parts if possible

## 🧪 API Documentation

### Base URL
- **Production**: `https://plant-disease-api-yt7l.onrender.com`
- **Local**: `http://localhost:8000`

### Endpoints

#### GET `/ping`
Health check endpoint

**Response:**
```json
"Hello, I am alive"
```

#### POST `/predict`
Predict disease from uploaded image

**Request:**
- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `file` (required): Image file (JPEG, PNG)
  - `crop` (optional): Crop type - `potato`, `pepper`, `tomato`, `maize`, `apple`, `wheat`, `rice`, `mango`, `sugarcane`, or `finger_millet` (default: `potato`)

**Example using curl:**
```bash
curl -X POST "https://plant-disease-api-yt7l.onrender.com/predict" \
  -F "file=@plant_image.jpg" \
  -F "crop=mango"
```

**Response:**
```json
{
  "class": "Mango_Anthracnose",
  "confidence": 0.9547,
  "crop": "mango",
  "all_predictions": {
    "Mango_Anthracnose": 0.9547,
    "Mango_Bacterial_Canker": 0.0012,
    "Mango_Cutting_Weevil": 0.0023,
    ...
  }
}
```

## 📊 Model Information

- **Architecture**: CNN (Convolutional Neural Network)
- **Framework**: TensorFlow 2.20.0 / Keras
- **Input Size**: 256x256 pixels (RGB)
- **Image Preprocessing**: 
  - EXIF orientation correction
  - RGB conversion
  - High-quality resizing (LANCZOS)
- **Training Dataset**: PlantVillage Dataset + Custom Datasets
- **Total Models**: 10 (one per crop type)

## 🎨 Technologies Used

### Backend
- **FastAPI** - Modern Python web framework
- **TensorFlow 2.20.0** - Deep learning inference
- **Pillow** - Image processing
- **Uvicorn** - ASGI server
- **NumPy** - Numerical operations

### Frontend
- **React 18.2.0** - UI framework
- **React Dropzone** - Drag & drop functionality
- **React Easy Crop** - Image cropping
- **Axios** - HTTP client
- **CSS3** - Modern responsive styling

### Deployment
- **Render** - Cloud platform (free tier)
- **Git/GitHub** - Version control

## 🚀 Deployment

### Frontend (Static Site)
- **Platform**: Render Static Site
- **Build Command**: `npm install && npm run build`
- **Publish Directory**: `build`
- **Auto-Deploy**: Enabled (on push to main)

### Backend (Web Service)
- **Platform**: Render Web Service
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`
- **Root Directory**: `backend`
- **Auto-Deploy**: Enabled (on push to main)

### Important Notes
- ⏱️ **Cold Start**: First request after inactivity may take 30-60 seconds (free tier limitation)
- 🔄 **Auto-Wake**: Backend automatically wakes up on request
- ⚡ **Subsequent Requests**: Fast response after initial wake-up

## 🔧 Configuration

### Environment Variables (Optional)

#### Frontend `.env` (for local development)
```
REACT_APP_API_URL=http://localhost:8000
```

#### Backend
No environment variables required. Models are loaded from relative paths.

### CORS Configuration
Backend allows all origins for production deployment:
```python
allow_origins=["*"]
```

## 🐛 Troubleshooting

### Backend Issues
- **TensorFlow errors**: Ensure Python 3.13+ and compatible TensorFlow version
- **Model not found**: Check model paths relative to project root
- **CUDA errors**: Expected on CPU-only systems, will fall back to CPU

### Frontend Issues
- **Cannot connect to backend**: Check if backend is running and URL is correct
- **Timeout errors**: Wait for backend cold start (up to 60 seconds)
- **Build errors**: Clear `node_modules` and reinstall: `rm -rf node_modules && npm install`

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👤 Author

**Suraj Singh**
- GitHub: [@surajsingh8204](https://github.com/surajsingh8204)
- Email: surajsingh8204@gmail.com

## 🙏 Acknowledgments

- **PlantVillage Dataset** - Training data for all crop disease models
- **TensorFlow Team** - Deep learning framework
- **FastAPI Community** - Modern web framework
- **React Community** - Frontend framework
- **Render** - Deployment platform

## 📸 Screenshots

### Desktop View
- Clean, modern interface with gradient background
- Category-based navigation (Vegetables, Fruits, Grains)
- Crop selector with emoji icons
- Drag & drop upload area
- Real-time disease detection results
- Treatment recommendations
- Crop-Disease reference list modal

### Mobile View
- Fully responsive layout
- Touch-friendly category tabs
- Compact crop buttons
- Camera capture with cropping
- Optimized disease list modal
- Smooth scrolling and transitions

### Tablet View
- Optimized layout for medium screens
- Comfortable touch targets
- Adaptive spacing and sizing

## 🔮 Future Enhancements

- [ ] Add more crop types (cotton, groundnut, etc.)
- [ ] Historical tracking of detections
- [ ] Batch image processing
- [ ] Export reports as PDF
- [ ] Multi-language support (Hindi, regional languages)
- [ ] Integration with agricultural LLM chatbot
- [ ] Weather-based disease prediction
- [ ] Offline mode with PWA
- [ ] Migration to DigitalOcean for 24/7 uptime
- [ ] User authentication and saved history

## 📊 Performance

- **Model Inference Time**: 5-10 seconds (after cold start)
- **Cold Start Time**: 30-60 seconds (free tier)
- **Prediction Accuracy**: Varies by crop (generally >90%)
- **Supported Image Formats**: JPEG, JPG, PNG

---

**Made with ❤️ for farmers and agricultural researchers**
