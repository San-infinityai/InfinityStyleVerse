# app/routes/admin_routes.py

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from ..models import User, Role, Permission
from ..database import db
from ..routes.auth_routes import role_required  # Adjust import path as needed
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


# --- USERS CRUD ---

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_all_users():
    users = User.query.all()
    result = []
    for user in users:
        result.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role.role_name if user.role else None,
            "status": user.status
        })
    return jsonify(result), 200


@admin_bp.route('/users', methods=['POST'])
@jwt_required()
@role_required('admin')
def create_user():
    data = request.get_json() or {}
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role_name = data.get('role', 'user')

    if not all([name, email, password]):
        return jsonify({"msg": "Missing required fields"}), 400

    # Check email uniqueness
    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already exists"}), 409

    # Validate role
    role_obj = Role.query.filter_by(role_name=role_name).first()
    if not role_obj:
        return jsonify({"msg": f"Role '{role_name}' does not exist"}), 400

    new_user = User(
        name=name,
        email=email,
        role=role_obj
    )
    new_user.password = password  # Will hash password using setter

    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"msg": "Database error creating user"}), 500

    return jsonify({"msg": "User created successfully", "user_id": new_user.id}), 201


@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def update_user(user_id):
    data = request.get_json() or {}
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Update fields if present
    email = data.get('email')
    role_name = data.get('role')
    name = data.get('name')
    password = data.get('password')

    if email:
        if User.query.filter(User.email == email, User.id != user_id).first():
            return jsonify({"msg": "Email already taken"}), 409
        user.email = email

    if role_name:
        role_obj = Role.query.filter_by(role_name=role_name).first()
        if not role_obj:
            return jsonify({"msg": f"Role '{role_name}' not found"}), 400
        user.role = role_obj

    if name:
        user.name = name

    if password:
        user.password = password  # Hash automatically

    db.session.commit()
    return jsonify({"msg": "User updated successfully"}), 200


@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "User deleted successfully"}), 200


# --- ROLES CRUD ---

@admin_bp.route('/roles', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_all_roles():
    roles = Role.query.all()
    result = []
    for role in roles:
        permissions = [{
            "id": perm.id,
            "system": perm.system,
            "module_access": perm.module_access
        } for perm in role.permissions]
        result.append({
            "id": role.id,
            "role_name": role.role_name,
            "permissions": permissions
        })
    return jsonify(result), 200


@admin_bp.route('/roles', methods=['POST'])
@jwt_required()
@role_required('admin')
def create_role():
    data = request.get_json() or {}
    role_name = data.get('role_name')
    permissions = data.get('permissions', [])

    if not role_name:
        return jsonify({"msg": "role_name is required"}), 400

    if Role.query.filter_by(role_name=role_name).first():
        return jsonify({"msg": "Role already exists"}), 409

    new_role = Role(role_name=role_name)
    db.session.add(new_role)
    db.session.flush()  # Get id without committing

    # Add permissions
    for perm in permissions:
        system = perm.get('system')
        module_access = perm.get('module_access')
        if not system or not module_access:
            db.session.rollback()
            return jsonify({"msg": "Invalid permissions format"}), 400
        new_perm = Permission(role_id=new_role.id, system=system, module_access=module_access)
        db.session.add(new_perm)

    db.session.commit()
    return jsonify({"msg": "Role created", "role_id": new_role.id}), 201


@admin_bp.route('/roles/<int:role_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def update_role(role_id):
    role = Role.query.get(role_id)
    if not role:
        return jsonify({"msg": "Role not found"}), 404

    data = request.get_json() or {}
    role_name = data.get('role_name')
    permissions = data.get('permissions')

    if role_name:
        # Check if new role_name is unique
        existing_role = Role.query.filter(Role.role_name == role_name, Role.id != role_id).first()
        if existing_role:
            return jsonify({"msg": "Role name already taken"}), 409
        role.role_name = role_name

    if permissions is not None:
        # Remove old permissions
        Permission.query.filter_by(role_id=role.id).delete()
        # Add new permissions
        for perm in permissions:
            system = perm.get('system')
            module_access = perm.get('module_access')
            if not system or not module_access:
                return jsonify({"msg": "Invalid permissions format"}), 400
            new_perm = Permission(role_id=role.id, system=system, module_access=module_access)
            db.session.add(new_perm)

    db.session.commit()
    return jsonify({"msg": "Role updated successfully"}), 200


@admin_bp.route('/roles/<int:role_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_role(role_id):
    role = Role.query.get(role_id)
    if not role:
        return jsonify({"msg": "Role not found"}), 404

    # Optionally: Check if any users assigned this role, disallow deletion if yes

    db.session.delete(role)
    db.session.commit()
    return jsonify({"msg": "Role deleted successfully"}), 200
