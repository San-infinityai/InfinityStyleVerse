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
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request
)
from ..models import Role
from ..models import TokenBlocklist

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity

def role_required(*allowed_roles):
    def outer(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # ensure token present & valid
            verify_jwt_in_request()
            claims = get_jwt()
            token_role = claims.get("role")
            if token_role and token_role in allowed_roles:
                return fn(*args, **kwargs)
            # fallback: check DB for up-to-date role
            user_id = get_jwt_identity()
            user = User.query.get(int(user_id))

            if user and user.role and user.role.role_name in allowed_roles:
                return fn(*args, **kwargs)
            return jsonify({"msg": "Forbidden - missing role"}), 403
        return wrapper
    return outer



# Set up logging
logging.basicConfig(level=logging.INFO)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json() or {}
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role_name = data.get('role', 'user')

        if not all([name, email, password]):
            return jsonify({"msg": "Missing required fields"}), 400

        # use db.session consistently
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"msg": "Email already registered"}), 409

        # find or create role
        role_obj = Role.query.filter_by(role_name=role_name).first()
        if not role_obj:
            role_obj = Role(role_name=role_name)
            db.session.add(role_obj)
            db.session.commit()   # commit to get id

        new_user = User(
            name=name,
            email=email,
            role=role_obj   # assign the Role instance (relationship)
        )
        new_user.password = password

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"msg": "User registered successfully"}), 201

    except Exception as e:
        logging.error("Registration error: %s", str(e))
        return jsonify({"msg": "Internal server error"}), 500



from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    get_jwt_identity, get_jwt
)
from datetime import datetime, timedelta

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json() or {}
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if not user or not user.verify_password(password):
            return jsonify({"msg": "Bad email or password"}), 401

        now = datetime.utcnow()
        threshold = timedelta(days=30)

        # Update last login and status
        if user.last_login and (now - user.last_login) <= threshold:
            user.status = "Active"
        else:
            user.status = "Inactive"

        user.last_login = now
        db.session.commit()

        # put role name in token claims
        role_name = user.role.role_name if user.role else "user"
        additional_claims = {"role": role_name}

        access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims, fresh=True)
        refresh_token = create_refresh_token(identity=str(user.id), additional_claims=additional_claims)

        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": role_name,
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
        "role": user.role.role_name if user.role else None,
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
        role_obj = Role.query.filter_by(role_name=role).first()
    if role_obj:
        user.role = role_obj
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

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    role_name = user.role.role_name if user.role else "user"
    new_access = create_access_token(identity=str(user.id), additional_claims={"role": role_name}, fresh=False)
    return jsonify(access_token=new_access), 200

@auth_bp.route('/logout_access', methods=['DELETE'])
@jwt_required()
def logout_access():
    jti = get_jwt()["jti"]
    db.session.add(TokenBlocklist(jti=jti, token_type="access", user_id=get_jwt_identity()))
    db.session.commit()
    return jsonify({"msg": "Access token revoked"}), 200

@auth_bp.route('/logout_refresh', methods=['DELETE'])
@jwt_required(refresh=True)
def logout_refresh():
    jti = get_jwt()["jti"]
    db.session.add(TokenBlocklist(jti=jti, token_type="refresh", user_id=get_jwt_identity()))
    db.session.commit()
    return jsonify({"msg": "Refresh token revoked"}), 200