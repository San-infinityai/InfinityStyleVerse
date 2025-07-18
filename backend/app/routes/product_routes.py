import base64
from flask import Blueprint, request, jsonify
from ..models import Product, ProductImage
from ..database import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

product_bp = Blueprint('product', __name__, url_prefix='/product')


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

    image_records = []
    for img in images:
        image_data = img.read()
        if not image_data:
            return jsonify({"error": f"Empty image file: {img.filename}"}), 400
        image_records.append(ProductImage(
            image_data=image_data  # Removed invalid filename argument here
        ))

    current_user_id = get_jwt_identity()

    new_product = Product(
        title=title,
        brand=brand,
        category=category,
        description=description,
        sale_price=float(sale_price) if sale_price else None,
        discount=float(discount) if discount else None,
        sizes=size,
        colors=color,
        tags=tag,
        visibility=visibility,
        publish_date=publish_date,
        user_id=current_user_id,
        esg_score=0.0,
        likes=0,
        views=0,
        images=image_records 
    )

    db.session.add(new_product)
    db.session.commit()

    return jsonify({
        "msg": "Product uploaded successfully",
        "product": new_product.to_dict()
    }), 201


@product_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()
    current_user = get_jwt_identity()

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


@product_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({"msg": f"Product with id {product_id} deleted successfully"}), 200


@product_bp.route('', methods=['GET'])
def get_products():
    try:
        limit = int(request.args.get('limit', 10))
        offset = int(request.args.get('offset', 0))
    except ValueError:
        return jsonify({"error": "Invalid limit or offset"}), 400

    products_query = Product.query.limit(limit).offset(offset).all()

    products_list = [p.to_dict() for p in products_query]

    return jsonify({
        "products": products_list,
        "limit": limit,
        "offset": offset
    }), 200

@product_bp.route("/my-products", methods=["GET"])
@jwt_required()
def get_my_products():
    current_user_id = get_jwt_identity()
    products = Product.query.filter_by(user_id=current_user_id).all()
    return jsonify([
        {
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "sale_price": p.sale_price,
            "category": p.category,
            "brand": p.brand,
            "images": [
                "data:image/jpeg;base64," + base64.b64encode(img.image_data).decode('utf-8')
                for img in p.images
            ]
        }
        for p in products
    ])
