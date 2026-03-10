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
from flask_jwt_extended import JWTManager
import secrets

load_dotenv()

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

# JWT Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', secrets.token_hex(32))
# For production use a longer expiration time or refresh tokens
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
jwt = JWTManager(app)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
DATA_GOV_API_KEY ="579b464db66ec23bdd000001cc455d6e413f41be71099b0155cd9bd2"
#DATA_GOV_API_KEY = os.getenv("DATA_GOV_API_KEY")

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Register Blueprints
from auth.auth_routes import auth_bp
from routes.disease_routes import disease_bp
from routes.weather_routes import weather_bp
from routes.market_routes import market_bp
from routes.advisory_routes import advisory_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(disease_bp, url_prefix='/api/disease')
app.register_blueprint(weather_bp, url_prefix='/api/weather')
app.register_blueprint(market_bp, url_prefix='/api/market-prices')
app.register_blueprint(advisory_bp, url_prefix='/api/advisory')

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


    
if __name__ == '__main__':
    print("🌱 AgroSense Backend Server Starting...")
    print("📡 API will be available at: http://localhost:5000")
    print("📚 API Documentation: http://localhost:5000/api/health")
    app.run(debug=True, host='0.0.0.0', port=5000)
