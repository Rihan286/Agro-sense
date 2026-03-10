from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import io
import datetime
from bson import ObjectId
from database import detection_history_collection
from ml.inference import preprocess_image, predict

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

disease_bp = Blueprint('disease', __name__)

@disease_bp.route('/detect', methods=['POST'])
@jwt_required()
def detect_disease():
    """Disease detection endpoint with DB logging"""
    try:
        farmer_id = get_jwt_identity()

        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400
        
        file = request.files['image']
        
        # Validate file type
        allowed_extensions = {'png', 'jpg', 'jpeg'}
        if '.' not in file.filename or \
           file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return jsonify({"error": "Invalid file type. Use PNG, JPG, or JPEG"}), 400
        
        img_bytes = file.read()
        
        # Read and preprocess image
        img_array = preprocess_image(io.BytesIO(img_bytes))
        
        # Predict disease
        predicted_class, confidence = predict(img_array)
        disease_name = CLASS_NAMES.get(predicted_class, "Unknown")
        final_confidence = round(confidence * 100, 2)
        
        # Determine crop (From disease name or input. Hardcoded logic for now)
        crop_name = disease_name.split()[0] if disease_name != "Unknown" else "Unknown"

        # Note: Ideally image should be saved to S3 or a local folder and URL stored.
        # For simplicity based on prompt, let's pretend we have a path or save it logically.
        image_path = f"/uploads/{file.filename}"

        if detection_history_collection is not None:
            # Save history to MongoDB
            detection_record = {
                "farmer_id": ObjectId(farmer_id),
                "crop": crop_name,
                "disease": disease_name,
                "confidence": final_confidence,
                "image_path": image_path,
                "timestamp": datetime.datetime.now()
            }
            detection_history_collection.insert_one(detection_record)
        
        response = {
            "success": True,
            "prediction": {
                "disease": disease_name,
                "confidence": final_confidence
            },
            "visualization": {},
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({"error": str(e), "type": "server_error"}), 500


@disease_bp.route('/history', methods=['GET'])
@jwt_required()
def get_disease_history():
    """Fetch history of detections for the logged-in user"""
    try:
        farmer_id = get_jwt_identity()
        
        if detection_history_collection is None:
            return jsonify({"error": "Database not connected"}), 500

        history_cursor = detection_history_collection.find({"farmer_id": ObjectId(farmer_id)}).sort("timestamp", -1)
        history_list = []
        for record in history_cursor:
            record['_id'] = str(record['_id'])
            record['farmer_id'] = str(record['farmer_id'])
            # Convert datetime to string
            if 'timestamp' in record:
                record['timestamp'] = record['timestamp'].isoformat()
            history_list.append(record)

        return jsonify({"success": True, "history": history_list}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
