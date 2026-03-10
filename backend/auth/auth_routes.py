from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import bcrypt
from database import farmers_collection
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    """Register a new farmer account"""
    # If MongoDB is not connected
    if farmers_collection is None:
        return jsonify({"success": False, "error": "Database connection failed"}), 500

    data = request.json
    
    # Validate required fields
    required_fields = ['name', 'email', 'password', 'phone', 'location']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"success": False, "error": f"Missing required field: {field}"}), 400
            
    # Check if email already exists
    if farmers_collection.find_one({"email": data['email']}):
        return jsonify({"success": False, "error": "Email already registered"}), 400
        
    try:
        # Hash password
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        
        # Create farmer document
        farmer = {
            "name": data['name'],
            "email": data['email'],
            "password": hashed_password.decode('utf-8'),
            "phone": data['phone'],
            "location": data['location'],
            "created_at": datetime.now()
        }
        
        # Insert into database
        farmers_collection.insert_one(farmer)
        
        return jsonify({"success": True, "message": "Account created successfully"}), 201
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login and receive JWT token"""
    if farmers_collection is None:
        return jsonify({"success": False, "error": "Database connection failed"}), 500

    data = request.json
    
    if not data.get('email') or not data.get('password'):
        return jsonify({"success": False, "error": "Email and password are required"}), 400
        
    try:
        # Find user
        farmer = farmers_collection.find_one({"email": data['email']})
        
        # Verify user exists and password is correct
        if not farmer or not bcrypt.checkpw(data['password'].encode('utf-8'), farmer['password'].encode('utf-8')):
            return jsonify({"success": False, "error": "Invalid email or password"}), 401
            
        # Create JWT token (use string representation of ObjectId)
        access_token = create_access_token(identity=str(farmer['_id']))
        
        # Remove password from response
        farmer_data = {
            "id": str(farmer['_id']),
            "name": farmer['name'],
            "email": farmer['email'],
            "phone": farmer.get('phone', ''),
            "location": farmer.get('location', '')
        }
        
        return jsonify({
            "success": True, 
            "token": access_token,
            "user": farmer_data
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logout (Client-side mainly, but we can return success)
    Note: For true logout with JWT, you could implement token blocklisting.
    Here we just rely on client clearing the token.
    """
    return jsonify({"success": True, "message": "Successfully logged out"}), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get the currently logged-in farmer's profile"""
    try:
        farmer_id = get_jwt_identity()
        from bson import ObjectId
        
        farmer = farmers_collection.find_one({"_id": ObjectId(farmer_id)})
        
        if not farmer:
            return jsonify({"success": False, "error": "User not found"}), 404
            
        farmer_data = {
            "id": str(farmer['_id']),
            "name": farmer['name'],
            "email": farmer['email'],
            "phone": farmer.get('phone', ''),
            "location": farmer.get('location', '')
        }
        
        return jsonify({"success": True, "user": farmer_data}), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
