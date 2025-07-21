# app/routes/auth.py

from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import logging
import os
import base64
from datetime import datetime, timedelta
from ..models import User, Product, Design
from ..database import get_db_session, db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Set up logging
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

        now = datetime.utcnow()
        threshold = timedelta(days=30)

        # Update last login and status
        if user.last_login and now - user.last_login <= threshold:
            user.status = "Active"
        else:
            user.status = "Inactive"

        user.last_login = now
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

    # Encode profile image
    if user.image_url:
        b64_data = base64.b64encode(user.image_url).decode('utf-8')
        profile_image_url = f"data:{user.image_mime};base64,{b64_data}"
    else:
        profile_image_url = "/static/images/default-profile.png"

    # Count designs and products
    design_count = Design.query.filter_by(user_id=user.id).count()
    product_count = Product.query.filter_by(user_id=user.id).count()

    return jsonify({
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "bio": user.bio or "",
        "profile_image_url": profile_image_url,
        "design_count": design_count,
        "saved_count": product_count
    })


@auth_bp.route('/update_profile', methods=['POST'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Get form data
    name = request.form.get("name")
    role = request.form.get("role")
    bio = request.form.get("bio")

    if name:
        user.name = name
    if role:
        user.role = role
    if bio is not None:
        user.bio = bio

    # Handle optional profile image
    if 'profile_image' in request.files:
        file = request.files['profile_image']
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            ext = os.path.splitext(filename)[1].lower()
            allowed_extensions = {".jpg", ".jpeg", ".png", ".gif"}
            if ext not in allowed_extensions:
                return jsonify({"msg": "Invalid file type"}), 400

            # Read file bytes
            file_data = file.read()
            mime_type = file.mimetype or "image/jpeg"

            # Store in database
            user.image_url = file_data
            user.image_mime = mime_type

    db.session.commit()

    return jsonify({"msg": "Profile updated successfully"})
