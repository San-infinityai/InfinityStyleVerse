# app/routes/auth.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from ..models import User, Product 
from ..database import get_db_session
from ..database import db 
import logging
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import render_template
import os
from werkzeug.utils import secure_filename
from backend.app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Set up logging (optional: configure to file)
logging.basicConfig(level=logging.INFO)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'user')  

        if not all([name, email, password]):
            return jsonify({"msg": "Missing required fields"}), 400

        session = next(get_db_session())

        existing_user = session.query(User).filter_by(email=email).first()
        if existing_user:
            return jsonify({"msg": "Email already registered"}), 409

        new_user = User(
            name=name,
            email=email,
            role=role
        )
        new_user.password = password 

        session.add(new_user)
        session.commit()

        return jsonify({"msg": "User registered successfully"}), 201

    except Exception as e:
        logging.error("Registration error: %s", str(e))
        return jsonify({"msg": "Internal server error"}), 500

        
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        from datetime import datetime, timedelta

        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if not user or not user.verify_password(password):
            return jsonify({"msg": "Bad email or password"}), 401

      
        user.last_login = datetime.utcnow()

        now = datetime.utcnow()
        threshold = timedelta(days=30)
        if user.last_login and now - user.last_login <= threshold:
            user.status = "Active"
        else:
            user.status = "Inactive"

        db.session.commit()  

        access_token = create_access_token(identity=str(user.id))

        return jsonify({
            "access_token": access_token,
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role,
                "last_login": user.last_login.strftime('%Y-%m-%d %H:%M:%S'),
                "status": user.status
            }
        }), 200

    except Exception as e:
        logging.error("Login error: %s", str(e))
        return jsonify({"msg": "Internal server error"}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Use getattr to safely get the image attribute or default
    profile_image_url = getattr(user, 'image', None) or '/static/images/profile.avif'

    return jsonify({
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "bio": user.bio or "",
        "profile_image_url": profile_image_url
    })