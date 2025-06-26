from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
from ..models.design import Design
from ..models.user import User
from ..database import db

design_bp = Blueprint('design_bp', __name__)

UPLOAD_FOLDER = 'static/uploads'  # relative to your Flask app root

@design_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_design():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    title = request.form.get('title')
    description = request.form.get('description')
    category = request.form.get('category')
    image_file = request.files.get('image')

    if not all([title, description, category, image_file]):
        return jsonify({'message': 'Missing required fields'}), 400

    filename = secure_filename(image_file.filename)

    upload_folder_abs = os.path.join(current_app.root_path, UPLOAD_FOLDER)
    if not os.path.exists(upload_folder_abs):
        os.makedirs(upload_folder_abs)

    image_path_abs = os.path.join(upload_folder_abs, filename)
    image_file.save(image_path_abs)

    image_path_db = os.path.join('uploads', filename)

    design = Design(
        title=title,
        description=description,
        category=category,
        image_url=image_path_db,  # <-- fixed here
        user_id=user.id
    )
    db.session.add(design)
    db.session.commit()

    return jsonify({'message': 'Design uploaded successfully'})

@design_bp.route('/my-designs', methods=['GET'])
@jwt_required()
def get_my_designs():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Optional: filter by category query param
    category = request.args.get('category')

    query = Design.query.filter_by(user_id=user_id)
    if category and category != 'All':
        query = query.filter_by(category=category)
    
    designs = query.all()

    designs_data = [
        {
            'id': d.id,
            'title': d.title,
            'description': d.description,
            'category': d.category,
            'image_url': d.image_url,
        }
        for d in designs
    ]

    return jsonify(designs_data)

@design_bp.route('/designs', methods=['GET'])
def get_all_designs():
    # Optional: filter by category query param
    category = request.args.get('category')

    query = Design.query
    if category and category != 'All':
        query = query.filter_by(category=category)
    
    designs = query.all()

    designs_data = [
        {
            'id': d.id,
            'title': d.title,
            'description': d.description,
            'category': d.category,
            'image_url': d.image_url,
            'user_id': d.user_id,
        }
        for d in designs
    ]

    return jsonify(designs_data)
