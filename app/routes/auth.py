# app/routes/auth.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.models import User, Product 
from app.database import get_db_session
from app.database import db 
import logging

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
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if not user or not user.verify_password(password):
            return jsonify({"msg": "Bad email or password"}), 401

        access_token = create_access_token(identity=user.id)
        return jsonify({
            "access_token": access_token,
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name
            }
        }), 200

    except Exception as e:
        logging.error("Login error: %s", str(e))
        return jsonify({"msg": "Internal server error"}), 500
