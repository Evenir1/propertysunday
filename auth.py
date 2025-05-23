# Auth Routes (User Registration and Login)
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt # PyJWT for token generation
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.user import User
# from main import db, app # db and app will be imported from main.py to avoid circular imports

# Placeholder for db and app.config, will be properly linked from main.py
class AppConfigPlaceholder:
    SECRET_KEY = os.environ.get("SECRET_KEY", "your_default_secret_key_for_dev")

class DBPlaceholder:
    session = None # This will be replaced by the actual db.session

db_placeholder = DBPlaceholder()
app_config_placeholder = AppConfigPlaceholder()

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"message": "Email and password are required"}), 400

    email = data["email"].lower()
    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists with this email"}), 409 # Conflict

    hashed_password = generate_password_hash(data["password"], method=	ext_style_placeholder="pbkdf2:sha256") # Explicitly state hashing method
    new_user = User(email=email, password_hash=hashed_password, full_name=data.get("full_name"))
    
    # The actual db object will be used here once linked from main.py
    # For now, we assume db_placeholder.session is the actual db.session
    if db_placeholder.session:
        db_placeholder.session.add(new_user)
        db_placeholder.session.commit()
    else:
        # This branch is for placeholder logic if db is not yet initialized
        # In a real scenario, this would raise an error or be handled by app initialization
        print(f"Simulating user registration: {new_user.to_dict()}") 
        # Simulate ID assignment for token generation if db is not available
        # This is highly simplified and for placeholder purposes only.
        # In a real app, the ID comes from the database after commit.
        if not hasattr(new_user, 'id') or not new_user.id:
             import random
             new_user.id = random.randint(1000,9999)

    # Generate a token for the new user
    token = jwt.encode({
        "user_id": new_user.id,
        "email": new_user.email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24) # Token expires in 24 hours
    }, app_config_placeholder.SECRET_KEY, algorithm="HS256")

    return jsonify({
        "message": "User registered successfully", 
        "user": new_user.to_dict(),
        "token": token
    }), 201

@auth_bp.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"message": "Email and password are required"}), 400

    email = data["email"].lower()
    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(data["password"]):
        return jsonify({"message": "Invalid email or password"}), 401

    # Generate token
    token = jwt.encode({
        "user_id": user.id,
        "email": user.email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, app_config_placeholder.SECRET_KEY, algorithm="HS256")

    return jsonify({
        "message": "Login successful", 
        "user": user.to_dict(),
        "token": token
    }), 200

# Note: To make this fully functional, these placeholders need to be resolved:
# 1. `db_placeholder.session` needs to be replaced with the actual `db.session` from the Flask app.
# 2. `User.query` needs to work with the actual `db` instance.
# 3. `app_config_placeholder.SECRET_KEY` needs to be the app's actual secret key.
# These will be linked when integrating this blueprint into the main Flask application (`main.py`).

