from flask import Flask, request, jsonify
from flask_cors import CORS
from ml.inference import preprocess_image,predict
import os
import numpy as np
from PIL import Image
import io
import base64
import requests
from datetime import datetime
import json
from ml.gemini_advisory import get_gemini_treatment
from dotenv import load_dotenv

def detect_intent(message):
    msg = message.lower().strip()

    greetings = ["hi", "hello", "hey", "namaste"]
    thanks = ["thanks", "thank you", "ok"]

    if msg in greetings:
        return "greeting"
    elif msg in thanks:
        return "thanks"
    elif "weather" in msg or "rain" in msg:
        return "weather"
    elif "price" in msg or "market" in msg:
        return "market"
    else:
        return "farming"


app = Flask(__name__)
CORS(app)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
DATA_GOV_API_KEY ="579b464db66ec23bdd000001cc455d6e413f41be71099b0155cd9bd2"
#DATA_GOV_API_KEY = os.getenv("DATA_GOV_API_KEY")


# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Disease class names
CLASS_NAMES = {
    0: "Chilli Anthracnose",
    1: "Chilli Cercospora",
    2: "Chilli Damping Off",
    3: "Chilli Healthy",
    4: "Chilli Leaf Curl Virus",
    5: "Chilli Mites and Thrips",
    6: "Chilli Powdery Mildew",
    7: "Chilli Veinal Mottle Virus",
    8: "Chilli Whitefly",
    9: "Chilli Yellowish"
}

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "AgroSense API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/detect-disease', methods=['POST'])
def detect_disease():
    """Disease detection endpoint"""
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400
        
        file = request.files['image']
        
        # Validate file type
        allowed_extensions = {'png', 'jpg', 'jpeg'}
        if '.' not in file.filename or \
           file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return jsonify({"error": "Invalid file type. Use PNG, JPG, or JPEG"}), 400
        
        img_bytes=file.read()
        
        # Read and preprocess image
        img_array=preprocess_image(io.BytesIO(img_bytes))
        predicted_class,confidence=predict(img_array)
        
        # Predict disease
        predicted_class, confidence = predict(img_array)
        disease_name = CLASS_NAMES.get(predicted_class, "Unknown")
        
        response = {
            "success": True,
            "prediction": {
                "disease": disease_name,
                "confidence": round(confidence * 100, 2)
            },
            "visualization": {},
            "timestamp": datetime.now().isoformat()
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e), "type": "server_error"}), 500

@app.route('/api/weather', methods=['GET'])
def get_weather():
    try:
        location = request.args.get('location', 'Bangalore')

        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHER_API_KEY}&units=metric"

        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            return jsonify({"success": False, "error": "City not found"}), 404

        weather_data = {
            "location": data["name"],
            "current": {
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "conditions": data["weather"][0]["description"],
                "wind_speed": data["wind"]["speed"],
                "uv_index": 5
            }
        }

        return jsonify({
            "success": True,
            "data": weather_data
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/market-prices', methods=['GET'])
def get_market_prices():
    try:
        crop = request.args.get('crop', 'tomato')

        url = f"https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?api-key={DATA_GOV_API_KEY}&format=json&filters[commodity]={crop}&limit=5"

        res = requests.get(url)
        data = res.json()

        records = data.get("records", [])

        if not records:
            return jsonify({"success": False, "error": "No market data found"})

        first = records[0]

        market_data = {
               "commodity": first["commodity"],
               "market": first["market"],   # mandi name
               "price": first["modal_price"],
               "min_price": first["min_price"],
               "max_price": first["max_price"],
               "avg_price": first["modal_price"],
                "top_markets": [
        {
            "name": r["market"],
            "price": r["modal_price"]
        } for r in records[:5]
    ],
    "recommendation": {
        "action": "HOLD",
        "reason": "Market stable"
    }
}

        return jsonify({"success": True, "data": market_data})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/advisory', methods=['POST'])
def get_advisory():
    try:
        data = request.json
        message = data.get("disease")

        if not message:
            return jsonify({"error": "Message required"}), 400
        
        intent = detect_intent(message)

        # -------- GREETING --------
        if intent == "greeting":
            return jsonify({
                "success": True,
                "reply": "Hello farmer 👋 How can I help you today?"
            })

        # -------- THANKS --------
        if intent == "thanks":
            return jsonify({
                "success": True,
                "reply": "You're welcome 🌱"
            })

        # -------- WEATHER --------
        if intent == "weather":
            return jsonify({
                "success": True,
                "reply": "Please check the weather section above ☁️"
            })

        # -------- MARKET --------
        if intent == "market":
            return jsonify({
                "success": True,
                "reply": "Please check market prices section 📈"
            })

        advice=get_gemini_treatment(message)

        return jsonify({
            "success": True,
            "disease": message,
            "advisory": advice,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    print("🌱 AgroSense Backend Server Starting...")
    print("📡 API will be available at: http://localhost:5000")
    print("📚 API Documentation: http://localhost:5000/api/health")
    app.run(debug=True, host='0.0.0.0', port=5000)
