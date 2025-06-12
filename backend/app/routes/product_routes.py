from flask import Blueprint, request, jsonify
from ..models import Product
from ..database import db

product_bp = Blueprint('product', __name__, url_prefix='/product')

# POST: Add a new product
@product_bp.route('', methods=['POST'])
def add_product():
    data = request.get_json()

    required_fields = ('title', 'category', 'description', 'image_url', 'user_id')
    if not all(k in data for k in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    new_product = Product(
        title=data['title'],
        category=data['category'],
        description=data['description'],
        image_url=data['image_url'],
        user_id=data['user_id'],
        esg_score=data.get('esg_score', 0.0),
        likes=data.get('likes', 0),
        views=data.get('views', 0)
    )

    db.session.add(new_product)
    db.session.commit()

    return jsonify({
        "msg": "Product uploaded successfully",
        "product": new_product.to_dict()
    }), 201


# GET: View all products, or filter by category
@product_bp.route('', methods=['GET'])
def get_products():
    category = request.args.get('category')
    query = Product.query

    if category:
        query = query.filter_by(category=category)

    products = query.all()
    return jsonify([product.to_dict() for product in products]), 200


# PUT: Update a product by ID
@product_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()
    # Update fields if they exist in data
    if 'title' in data:
        product.title = data['title']
    if 'category' in data:
        product.category = data['category']
    if 'description' in data:
        product.description = data['description']
    if 'image_url' in data:
        product.image_url = data['image_url']
    if 'user_id' in data:
        product.user_id = data['user_id']
    if 'esg_score' in data:
        product.esg_score = data['esg_score']
    if 'likes' in data:
        product.likes = data['likes']
    if 'views' in data:
        product.views = data['views']

    db.session.commit()

    return jsonify({
        "msg": "Product updated successfully",
        "product": product.to_dict()
    }), 200


# DELETE: Delete a product by ID
@product_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({"msg": f"Product with id {product_id} deleted successfully"}), 200
