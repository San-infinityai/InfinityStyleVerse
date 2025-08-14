# app/routes/admin_routes.py

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from ..models import User, Role, Permission
from ..database import db
from ..routes.auth_routes import role_required
from sqlalchemy.exc import IntegrityError

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


# --- USERS CRUD ---

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_all_users():
    """
    List all users (admin only)
    ---
    tags:
      - "Admin - Users"
    security:
      - BearerAuth: []
    x-roles:
      - admin
    responses:
      200:
        description: Array of users
        schema:
          type: array
          items:
            type: object
            properties:
              id: { type: integer }
              name: { type: string }
              email: { type: string }
              role: { type: string }
              status: { type: string }
      401:
        description: Missing/invalid token
      403:
        description: Forbidden (requires admin)
    """
    users = User.query.all()
    result = [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role.role_name if user.role else None,
            "status": user.status
        }
        for user in users
    ]
    return jsonify(result), 200


@admin_bp.route('/users', methods=['POST'])
@jwt_required()
@role_required('admin')
def create_user():
    """
    Create a user (admin only)
    ---
    tags:
      - "Admin - Users"
    security:
      - BearerAuth: []
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [name, email, password, role]
          properties:
            name: { type: string, example: "Bob" }
            email: { type: string, example: "bob@example.com" }
            password: { type: string, example: "BobStrong123!" }
            role: { type: string, example: "executive" }
    responses:
      201:
        description: User created successfully
      400:
        description: Missing or invalid data
      401:
        description: Unauthorized
      403:
        description: Forbidden
      409:
        description: Email already exists
    """
    data = request.get_json() or {}
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role_name = data.get('role', 'user')

    if not all([name, email, password]):
        return jsonify({"msg": "Missing required fields"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already exists"}), 409

    role_obj = Role.query.filter_by(role_name=role_name).first()
    if not role_obj:
        return jsonify({"msg": f"Role '{role_name}' does not exist"}), 400

    new_user = User(name=name, email=email, role=role_obj)
    new_user.password = password  # hashed automatically via setter

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
    """
    Update a user (admin only)
    ---
    tags:
      - "Admin - Users"
    security:
      - BearerAuth: []
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
          properties:
            name: { type: string }
            email: { type: string }
            password: { type: string }
            role: { type: string }
    responses:
      200:
        description: User updated
      400:
        description: Invalid data
      404:
        description: User not found
      409:
        description: Email already taken
    """
    data = request.get_json() or {}
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

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
        user.password = password

    db.session.commit()
    return jsonify({"msg": "User updated successfully"}), 200


@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_user(user_id):
    """
    Delete a user (admin only)
    ---
    tags:
      - "Admin - Users"
    security:
      - BearerAuth: []
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: User deleted
      404:
        description: User not found
    """
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
def list_roles():
    """
    List all roles with permissions (admin only)
    ---
    tags:
      - "Admin - Roles"
    security:
      - BearerAuth: []
    responses:
      200:
        description: List of roles
    """
    roles = Role.query.all()
    result = []
    for role in roles:
        permissions = [
            {"id": perm.id, "system": perm.system, "module_access": perm.module_access}
            for perm in role.permissions
        ]
        result.append({"id": role.id, "role_name": role.role_name, "permissions": permissions})
    return jsonify(result), 200


@admin_bp.route('/roles', methods=['POST'])
@jwt_required()
@role_required('admin')
def create_role():
    """
    Create a new role with permissions
    ---
    tags:
      - "Admin - Roles"
    security:
      - BearerAuth: []
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            role_name: { type: string, example: "brand_manager" }
            permissions:
              type: array
              items:
                type: object
                properties:
                  system: { type: string, example: "products" }
                  module_access: { type: string, example: "read_write" }
    responses:
      201:
        description: Role created
      400:
        description: Invalid input
      409:
        description: Role already exists
    """
    data = request.get_json() or {}
    role_name = data.get('role_name')
    permissions = data.get('permissions', [])

    if not role_name:
        return jsonify({"msg": "role_name is required"}), 400

    if Role.query.filter_by(role_name=role_name).first():
        return jsonify({"msg": "Role already exists"}), 409

    new_role = Role(role_name=role_name)
    db.session.add(new_role)
    db.session.flush()

    for perm in permissions:
        system = perm.get('system')
        module_access = perm.get('module_access')
        if not system or not module_access:
            db.session.rollback()
            return jsonify({"msg": "Invalid permissions format"}), 400
        db.session.add(Permission(role_id=new_role.id, system=system, module_access=module_access))

    db.session.commit()
    return jsonify({"msg": "Role created", "role_id": new_role.id}), 201


@admin_bp.route('/roles/<int:role_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def update_role(role_id):
    """
    Update a role and its permissions
    ---
    tags:
      - "Admin - Roles"
    security:
      - BearerAuth: []
    parameters:
      - name: role_id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
          properties:
            role_name: { type: string }
            permissions:
              type: array
              items:
                type: object
                properties:
                  system: { type: string }
                  module_access: { type: string }
    responses:
      200:
        description: Role updated
      404:
        description: Role not found
    """
    role = Role.query.get(role_id)
    if not role:
        return jsonify({"msg": "Role not found"}), 404

    data = request.get_json() or {}
    role_name = data.get('role_name')
    permissions = data.get('permissions')

    if role_name:
        existing_role = Role.query.filter(Role.role_name == role_name, Role.id != role_id).first()
        if existing_role:
            return jsonify({"msg": "Role name already taken"}), 409
        role.role_name = role_name

    if permissions is not None:
        Permission.query.filter_by(role_id=role.id).delete()
        for perm in permissions:
            system = perm.get('system')
            module_access = perm.get('module_access')
            if not system or not module_access:
                return jsonify({"msg": "Invalid permissions format"}), 400
            db.session.add(Permission(role_id=role.id, system=system, module_access=module_access))

    db.session.commit()
    return jsonify({"msg": "Role updated successfully"}), 200


@admin_bp.route('/roles/<int:role_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_role(role_id):
    """
    Delete a role
    ---
    tags:
      - "Admin - Roles"
    security:
      - BearerAuth: []
    parameters:
      - name: role_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Role deleted
      404:
        description: Role not found
    """
    role = Role.query.get(role_id)
    if not role:
        return jsonify({"msg": "Role not found"}), 404

    db.session.delete(role)
    db.session.commit()
    return jsonify({"msg": "Role deleted successfully"}), 200
