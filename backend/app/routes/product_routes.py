import os
from flask import Blueprint, request, jsonify
from ..models import Product
from ..database import db
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app
from flask import Blueprint, request, jsonify, url_for


product_bp = Blueprint('product', __name__, url_prefix='/product')

# Folder to save uploaded images (relative to your Flask app root)
UPLOAD_FOLDER = 'static/uploads'

def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_image(image_file):
    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        upload_folder = os.path.join(current_app.root_path, UPLOAD_FOLDER)
        os.makedirs(upload_folder, exist_ok=True)  # create folder if not exists
        save_path = os.path.join(upload_folder, filename)
        image_file.save(save_path)
        # Return relative URL for frontend usage
        return f'/{UPLOAD_FOLDER}/{filename}'
    else:
        raise ValueError("Invalid image file")

@product_bp.route('', methods=['POST'])
@jwt_required()
def add_product():
    title = request.form.get('product_name') or request.form.get('title')
    brand = request.form.get('brand')
    category = request.form.get('category')
    description = request.form.get('description')
    sale_price = request.form.get('sale_price')
    discount = request.form.get('discount')
    size = request.form.get('size')
    color = request.form.get('color')
    tag = request.form.get('tag')
    visibility = request.form.get('visibility', 'Published')
    publish_date_str = request.form.get('schedule_date')
    publish_date = datetime.strptime(publish_date_str, '%Y-%m-%d') if publish_date_str else None

    if not all([title, category, description]):
        return jsonify({"error": "Missing required fields"}), 400

    images = request.files.getlist('product_images[]')
    if len(images) < 4:
        return jsonify({"error": "At least 4 images are required"}), 400

    try:
        image_urls = []
        for image in images:
            saved_path = save_image(image)
            image_urls.append(saved_path)
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    image_url = image_urls[0]
    image_gallery = json.dumps(image_urls[1:]) if len(image_urls) > 1 else json.dumps([])

    current_user_id = get_jwt_identity()

    new_product = Product(
        title=title,
        brand=brand,
        category=category,
        description=description,
        sale_price=sale_price,
        discount=discount,
        sizes=size,
        colors=color,
        tags=tag,
        image_url=image_url,
        image_gallery=image_gallery,
        visibility=visibility,
        publish_date=publish_date,
        user_id=current_user_id,
        esg_score=0.0,
        likes=0,
        views=0
    )

    db.session.add(new_product)
    db.session.commit()

    return jsonify({"msg": "Product uploaded successfully", "product": new_product.to_dict()}), 201

# PUT: Update a product by ID
@product_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()
    current_user = get_jwt_identity()

    # Field updates
    if 'title' in data:
        product.title = data['title']
    if 'brand' in data:
        product.brand = data['brand']
    if 'category' in data:
        product.category = data['category']
    if 'description' in data:
        product.description = data['description']
    if 'sale_price' in data:
        product.sale_price = data['sale_price']
    if 'discount' in data:
        product.discount = data['discount']
    if 'sizes' in data:
        product.sizes = ','.join(data['sizes'])
    if 'colors' in data:
        product.colors = ','.join(data['colors'])
    if 'tags' in data:
        product.tags = ','.join(data['tags'])
    if 'image_url' in data:
        product.image_url = data['image_url']
    if 'image_gallery' in data:
        product.image_gallery = json.dumps(data['image_gallery'])
    if 'visibility' in data:
        product.visibility = data['visibility']
    if 'publish_date' in data:
        product.publish_date = datetime.strptime(data['publish_date'], '%Y-%m-%d') if data['publish_date'] else None
    if 'esg_score' in data:
        product.esg_score = data['esg_score']
    if 'likes' in data:
        product.likes = data['likes']
    if 'views' in data:
        product.views = data['views']

    db.session.commit()

    return jsonify({"msg": "Product updated successfully", "product": product.to_dict()}), 200


# DELETE: Delete a product by ID
@product_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    current_user = get_jwt_identity()

    db.session.delete(product)
    db.session.commit()

    return jsonify({"msg": f"Product with id {product_id} deleted successfully"}), 200


@product_bp.route('', methods=['GET'])
def get_products():
    # Get limit and offset from query parameters, with defaults
    try:
        limit = int(request.args.get('limit', 10))
        offset = int(request.args.get('offset', 0))
    except ValueError:
        return jsonify({"error": "Invalid limit or offset"}), 400

    # Query products with pagination
    products_query = Product.query.limit(limit).offset(offset).all()

    products_list = []
    for p in products_query:
        products_list.append({
            "id": p.id,
            "title": p.title,
            "brand": p.brand,
            "category": p.category,
            "description": p.description,
            "sale_price": p.sale_price,
            "discount": p.discount,
            "sizes": p.sizes.split(',') if p.sizes else [],
            "colors": p.colors.split(',') if p.colors else [],
            "tags": p.tags.split(',') if p.tags else [],
            # Use product image URL or fallback to placeholder
            "image_url": p.image_url if p.image_url else url_for('static', filename='images/placeholder.png', _external=True),
            "image_gallery": json.loads(p.image_gallery) if p.image_gallery else [],
            "visibility": p.visibility,
            "publish_date": p.publish_date.strftime('%Y-%m-%d') if p.publish_date else None,
            "esg_score": p.esg_score,
            "likes": p.likes,
            "views": p.views
        })

    return jsonify({
        "products": products_list,
        "limit": limit,
        "offset": offset
    }), 200