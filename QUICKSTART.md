# 🚀 Quick Start Guide

## Get AgroSense Running in 5 Minutes

### Step 1: Install Dependencies (2 minutes)

```bash
cd agrosense/backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Configure API Keys (1 minute)

```bash
# Copy example environment file
cp .env.example .env

# Edit with your API key (optional for demo)
# The app works with simulated data without API keys
nano .env
```

### Step 3: Start Backend (30 seconds)

```bash
# From backend directory
python app.py
```

You should see:
```
🌱 AgroSense Backend Server Starting...
📡 API will be available at: http://localhost:5000
 * Running on http://0.0.0.0:5000
```

### Step 4: Open Frontend (30 seconds)

**Option A: Direct Browser**
```bash
# From frontend directory
open index.html
# or double-click index.html
```

**Option B: Python Server (Recommended)**
```bash
# Open new terminal
cd agrosense/frontend
python -m http.server 8000
```

Then open browser to: `http://localhost:8000`

### Step 5: Test the Application (1 minute)

1. **Disease Detection**
   - Click "Upload Image" 
   - Select any plant leaf image
   - Click "Detect Disease"
   - View results with confidence and treatment

2. **Weather Advisory**
   - Enter a location (e.g., "Bangalore")
   - Click "Get Weather"
   - View weather and farming advisories

3. **Market Intelligence**
   - Select a crop from dropdown
   - Click "Get Prices"
   - View market prices and recommendations

4. **AI Assistant**
   - Type a farming question
   - Click "Send"
   - Get AI-powered advice

---

## Sample Plant Images for Testing

If you don't have plant images, you can:
1. Download sample images from PlantVillage dataset
2. Use any leaf photo from your phone
3. Search online for "tomato leaf disease" images

---

## Troubleshooting

### Backend won't start
```bash
# Check if port 5000 is in use
lsof -i :5000

# Try a different port
python app.py --port 5001
```

### Frontend can't connect to backend
1. Ensure backend is running at http://localhost:5000
2. Check browser console for errors (F12)
3. Verify CORS is enabled in backend

### Module not found errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## What's Next?

### For Development
1. Read `docs/API_DOCUMENTATION.md` for API details
2. Check `docs/DEPLOYMENT_GUIDE.md` for production setup
3. Customize the disease classes in `backend/app.py`
4. Train your own ML model for better accuracy

### For Production
1. Get real API keys:
   - OpenWeatherMap: https://openweathermap.org/api
2. Train and integrate actual ML model
3. Setup proper database
4. Deploy to cloud (AWS, GCP, Azure)
5. Enable HTTPS
6. Implement user authentication

---

## Project Structure

```
agrosense/
├── backend/              # Flask API
│   ├── app.py           # Main application
│   ├── requirements.txt # Dependencies
│   └── .env.example     # Config template
├── frontend/            # Web interface
│   ├── index.html       # Main page
│   ├── css/styles.css   # Styling
│   └── js/main.js       # Functionality
├── docs/                # Documentation
│   ├── API_DOCUMENTATION.md
│   └── DEPLOYMENT_GUIDE.md
└── README.md            # Project overview
```

---

## Features Checklist

- [x] Disease Detection with CNN
- [x] Grad-CAM Visualization
- [x] Weather Integration
- [x] Market Price Analysis
- [x] AI Chat Assistant
- [x] Responsive Design
- [x] REST API
- [ ] Mobile App (Future)
- [ ] Real ML Model Integration
- [ ] User Authentication
- [ ] Database Integration

---

## Need Help?

1. Check `README.md` for detailed information
2. Review `docs/` folder for documentation
3. Contact team members (see README)

---

**Happy Farming! 🌱**

Last Updated: February 2024
