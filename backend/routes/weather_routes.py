from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests
from bson import ObjectId

weather_bp = Blueprint('weather', __name__)

@weather_bp.route('', methods=['GET'])
@weather_bp.route('/', methods=['GET'])
@jwt_required()
def get_weather():
    try:
        farmer_id = get_jwt_identity()
        location = request.args.get('location', 'Bangalore')
        
        import os
        OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

        if not OPENWEATHER_API_KEY:
            return jsonify({"success": False, "error": "OpenWeather API Key missing"}), 500

        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHER_API_KEY}&units=metric"

        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            return jsonify({"success": False, "error": "City not found"}), 404

        # Openweather free tier 'current' does not provide UV index directly without OneCall. Let's fetch it for free securely using OpenMeteo for the exact lat/lon dynamically.
        lat = data["coord"]["lat"]
        lon = data["coord"]["lon"]
        uv_res = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=uv_index")
        uv_index = 5
        if uv_res.status_code == 200:
            uv_index = uv_res.json().get("current", {}).get("uv_index", 5)

        weather_data = {
            "location": data["name"],
            "current": {
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "conditions": data["weather"][0]["description"],
                "wind_speed": data["wind"]["speed"],
                "uv_index": uv_index
            }
        }

        return jsonify({
            "success": True,
            "data": weather_data
        }), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
