# app/routes/admin_routes.py

from flask import Blueprint, jsonify, request
from ..models import User
from ..database import get_db_session
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/users', methods=['GET'])
def get_all_users():
    session = next(get_db_session())
    users = session.query(User).all()
    now = datetime.utcnow()
    threshold = timedelta(days=30)

    result = []
    for user in users:
        status = "Inactive"
        if user.last_login and now - user.last_login <= threshold:
            status = "Active"

        result.append({
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "status": status
        })
    return jsonify(result)


@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    session = next(get_db_session())
    user = session.query(User).get(user_id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    user.email = data.get('email', user.email)
    user.role = data.get('role', user.role)
    session.commit()
    return jsonify({"msg": "User updated successfully"}), 200


@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    session = next(get_db_session())
    user = session.query(User).get(user_id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    session.delete(user)
    session.commit()
    return jsonify({"msg": "User deleted successfully"}), 200
