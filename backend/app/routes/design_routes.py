from flask import Blueprint, request, jsonify, Response
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

    allowed_mime_types = ['image/png', 'image/jpeg']
    if image_file.mimetype not in allowed_mime_types:
        return jsonify({'message': 'Only PNG and JPEG images are allowed'}), 400

    filename = image_file.filename.lower()
    allowed_extensions = ['.png', '.jpg', '.jpeg']
    if not any(filename.endswith(ext) for ext in allowed_extensions):
        return jsonify({'message': 'Invalid file extension'}), 400

    image_data = image_file.read()

    design = Design(
        title=title,
        description=description,
        category=category,
        image_url=image_data,  
        image_mime=image_file.mimetype,
        user_id=user.id
    )
    try:
        db.session.add(design)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to save design', 'error': str(e)}), 500

    return jsonify({'message': 'Design uploaded successfully', 'id': design.id})


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
        encoded_image = base64.b64encode(d.image_url).decode('utf-8')
        image_data_url = f"data:{d.image_mime};base64,{encoded_image}"

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
        encoded_image = base64.b64encode(d.image_url).decode('utf-8')
        image_data_url = f"data:{d.image_mime};base64,{encoded_image}"

        designs_data.append({
            'id': d.id,
            'title': d.title,
            'description': d.description,
            'category': d.category,
            'image_data_url': image_data_url,
            'user_id': d.user_id
        })

    return jsonify(designs_data)


@design_bp.route('/design-image/<int:design_id>', methods=['GET'])
def get_design_image(design_id):
    """
    Serve raw binary image for <img src="/api/design-image/1"> usage.
    """
    design = Design.query.get(design_id)
    if not design:
        return jsonify({'message': 'Design not found'}), 404

    return Response(design.image_url, mimetype=design.image_mime)

@design_bp.route('/designs/<int:design_id>', methods=['PUT'])
@jwt_required()
def update_design(design_id):
    user_id = get_jwt_identity()
    design = Design.query.get(design_id)

    if not design:
        return jsonify({'message': 'Design not found'}), 404

    if design.user_id != int(user_id):
        return jsonify({'message': 'Unauthorized'}), 403

    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    title = data.get('title')
    description = data.get('description')
    category = data.get('category')

    if title:
        design.title = title
    if description:
        design.description = description
    if category:
        design.category = category

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update design', 'error': str(e)}), 500

    return jsonify({'message': 'Design updated successfully'})


@design_bp.route('/designs/<int:design_id>', methods=['DELETE'])
@jwt_required()
def delete_design(design_id):
    user_id = get_jwt_identity()
    design = Design.query.get(design_id)

    if not design:
        return jsonify({'message': 'Design not found'}), 404

    if design.user_id != int(user_id):
        return jsonify({'message': 'Unauthorized'}), 403

    try:
        db.session.delete(design)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to delete design', 'error': str(e)}), 500

    return jsonify({'message': 'Design deleted successfully'})
