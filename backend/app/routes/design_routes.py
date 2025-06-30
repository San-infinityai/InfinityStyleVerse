from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import base64

from ..models.design import Design
from ..models.user import User
from ..database import db

design_bp = Blueprint('design_bp', __name__)

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

    # Validate MIME type
    allowed_mime_types = ['image/png', 'image/jpeg','image/jpg']
    if image_file.mimetype not in allowed_mime_types:
        return jsonify({'message': 'Only PNG and JPEG images are allowed'}), 400

    # Validate extension (optional extra safety)
    allowed_extensions = ['.png', '.jpg', '.jpeg']
    filename = image_file.filename.lower()
    if not any(filename.endswith(ext) for ext in allowed_extensions):
        return jsonify({'message': 'Invalid file extension'}), 400

    # Read image bytes
    image_data = image_file.read()

    design = Design(
        title=title,
        description=description,
        category=category,
        image_url=image_data,  # correct variable here
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

    category = request.args.get('category')

    query = Design.query.filter_by(user_id=user_id)
    if category and category != 'All':
        query = query.filter_by(category=category)
    
    designs = query.all()

    designs_data = []
    for d in designs:
        image_data = d.image_url
        # Fix if image_data is string (convert to bytes)
        if isinstance(image_data, str):
            image_data = image_data.encode('utf-8')

        encoded_image = base64.b64encode(image_data).decode('utf-8')
        image_data_url = f"data:image/jpg;base64,{encoded_image}"

        designs_data.append({
            'id': d.id,
            'title': d.title,
            'description': d.description,
            'category': d.category,
            'image_data_url': image_data_url
        })

    return jsonify(designs_data)


@design_bp.route('/designs', methods=['GET'])
def get_all_designs():
    category = request.args.get('category')

    query = Design.query
    if category and category != 'All':
        query = query.filter_by(category=category)
    
    designs = query.all()

    designs_data = []
    for d in designs:
        image_data = d.image_url
        if isinstance(image_data, str):
            image_data = image_data.encode('utf-8')

        encoded_image = base64.b64encode(image_data).decode('utf-8')
        image_data_url = f"data:image/jpeg;base64,{encoded_image}"

        designs_data.append({
            'id': d.id,
            'title': d.title,
            'description': d.description,
            'category': d.category,
            'image_data_url': image_data_url,
            'user_id': d.user_id
        })

    return jsonify(designs_data)
