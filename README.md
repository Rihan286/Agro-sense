# 🌱 AgroSense - AI Plant Disease Detector

An AI-driven solution designed to assist farmers in detecting crop diseases using computer vision and providing intelligent, personalized agricultural advisory.

## 📋 Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Team](#team)

## ✨ Features

### 🔬 Disease Detection
- Real-time plant disease detection using deep learning (CNN)
- Support for multiple crops (Apple, Tomato, Potato, etc.)
- Grad-CAM visualization for explainability
- 95%+ accuracy on PlantVillage dataset

### 🌤️ Weather Integration
- Real-time weather data via OpenWeatherMap API
- Location-based weather advisories
- Agricultural recommendations based on weather conditions

### 💰 Market Intelligence
- Live market price tracking (Agmarknet integration)
- Price trend analysis and forecasting
- Best market recommendations

### 🤖 AI Advisory System
- LLM-powered Q&A system
- Multilingual support
- Context-aware farming recommendations
- Treatment and prevention guidance

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask (Python 3.8+)
- **ML/DL**: TensorFlow/Keras, OpenCV
- **APIs**: OpenWeatherMap, Agmarknet
- **Image Processing**: Pillow, NumPy

### Frontend
- **HTML5**, **CSS3**, **JavaScript (ES6+)**
- **Responsive Design**
- **Real-time API Integration**

### Machine Learning
- **Model**: CNN (Convolutional Neural Network)
- **Dataset**: PlantVillage, PlantDoc
- **Explainability**: Grad-CAM
- **Framework**: TensorFlow 2.x

## 📁 Project Structure

```
agrosense/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── config.py             # Configuration settings
│   ├── models/
│   │   ├── disease_model.py  # Disease detection model
│   │   └── gradcam.py        # Grad-CAM implementation
│   ├── routes/
│   │   ├── disease.py        # Disease detection routes
│   │   ├── weather.py        # Weather API routes
│   │   └── market.py         # Market data routes
│   └── utils/
│       ├── image_processing.py
│       └── api_helpers.py
├── frontend/
│   ├── index.html            # Main web interface
│   ├── css/
│   │   └── styles.css        # Styling
│   ├── js/
│   │   ├── main.js          # Core functionality
│   │   └── api.js           # API calls
│   └── assets/
│       └── images/
├── docs/
│   ├── API_DOCUMENTATION.md
│   └── DEPLOYMENT_GUIDE.md
└── README.md
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Backend Setup

1. **Clone the repository**
```bash
cd agrosense/backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
Create a `.env` file in the backend directory:
```
OPENWEATHER_API_KEY=your_api_key_here
FLASK_ENV=development
SECRET_KEY=your_secret_key
```

5. **Run the backend server**
```bash
python app.py
```
Server will start at `http://localhost:5000`

### Frontend Setup

1. **Open the frontend**
Simply open `frontend/index.html` in a web browser, or use a local server:

```bash
cd frontend
python -m http.server 8000
```
Access at `http://localhost:8000`

## 💻 Usage

### Disease Detection
1. Open the web interface
2. Click on "Upload Image" in the Disease Detection section
3. Select a plant leaf image
4. Click "Detect Disease"
5. View results with disease name, confidence, and treatment recommendations

### Weather Advisory
1. Enter your location or use GPS
2. View current weather conditions
3. Get agricultural advisories based on weather

### Market Prices
1. Select your crop
2. View current market prices
3. Get selling recommendations and price forecasts

### AI Chat Assistant
1. Type your farming query
2. Get instant AI-powered advice
3. Ask follow-up questions for detailed guidance

## 📡 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### 1. Health Check
```http
GET /api/health
```

#### 2. Disease Detection
```http
POST /api/detect-disease
Content-Type: multipart/form-data

Parameters:
- image: File (required) - Plant leaf image
```

Response:
```json
{
  "success": true,
  "prediction": {
    "disease": "Tomato Early Blight",
    "confidence": 94.5,
    "severity": "Medium",
    "treatment": "Apply fungicides, improve air circulation"
  },
  "image": "base64_encoded_image",
  "timestamp": "2024-02-01T10:30:00"
}
```

#### 3. Weather Data
```http
GET /api/weather?lat=12.9716&lon=77.5946
```

#### 4. Market Prices
```http
GET /api/market-prices?crop=tomato
```

#### 5. AI Advisory
```http
POST /api/advisory
Content-Type: application/json

Body:
{
  "query": "How to treat early blight?",
  "context": {
    "crop": "tomato",
    "disease": "early_blight"
  }
}
```

## 👥 Team

- **Mahantesh M A** (22BBTCS167)
- **Mohammad Roshan M Nadaf** (22BBTCS176)
- **Mallik Rihan** (22BBTCS169)

**Guide**: Prof. Priyanka M, Assistant Professor

## 📊 Model Performance

- **Accuracy**: 96.3% on test set
- **Dataset**: PlantVillage (54,000+ images, 38 disease classes)
- **Model Architecture**: Custom CNN with transfer learning
- **Inference Time**: <500ms per image

## 🔮 Future Enhancements

1. **Mobile App**: Native Android/iOS applications
2. **Offline Mode**: Edge deployment for areas with limited connectivity
3. **Multi-crop Support**: Expand to 50+ crop varieties
4. **Drone Integration**: Aerial disease detection
5. **Blockchain**: Secure farm data management
6. **IoT Sensors**: Real-time soil and weather monitoring

## 📝 License

This project is developed as a capstone project for academic purposes.

## 🤝 Contributing

This is an academic project. For queries, please contact the team members.

## 📧 Contact

For any questions or support:
- Email: [your-email@example.com]
- Project Repository: [GitHub Link]

---

**Made with 🌱 by Team AgroSense**
