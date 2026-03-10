from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime
from bson import ObjectId
from database import advisory_history_collection
from ml.gemini_advisory import get_gemini_treatment

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

advisory_bp = Blueprint('advisory', __name__)

@advisory_bp.route('', methods=['POST'])
@advisory_bp.route('/', methods=['POST'])
@jwt_required()
def get_advisory():
    try:
        farmer_id = get_jwt_identity()
        data = request.json
        message = data.get("disease") # Can be disease name or general farming question

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

        advice = get_gemini_treatment(message)
        
        # Save advisory history
        if advisory_history_collection is not None:
            advisory_record = {
                "farmer_id": ObjectId(farmer_id),
                "disease": message,
                "advisory_text": advice,
                "created_at": datetime.datetime.now()
            }
            advisory_history_collection.insert_one(advisory_record)

        return jsonify({
            "success": True,
            "disease": message,
            "advisory": advice,
            "timestamp": datetime.datetime.now().isoformat()
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
