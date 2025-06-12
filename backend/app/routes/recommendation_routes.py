# backend/app/routes/recommendation_routes.py

from flask import Blueprint, jsonify
import pickle
from ..models.product import Product

recommendation_bp = Blueprint('recommendation', __name__, url_prefix='/api')

# Load the model and data once when the module loads
with open(r'C:\xampp\htdocs\infinitystyleverse\models\recommender_model.pkl', 'rb') as f:
    model_data = pickle.load(f)
    df = model_data['df']  # DataFrame with product info
    similarities = model_data['similarities']  # similarity matrix

print("DataFrame columns are:", df.columns)

def get_similar_products(index):
    scores = list(enumerate(similarities[index]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    top_3 = scores[1:4]  # skip the product itself (index 0)
    return [(df['title'][i], score) for i, score in top_3]

@recommendation_bp.route('/recommend/<int:pid>', methods=['GET'])
def recommend_product(pid):  # Renamed function here
    product = Product.query.get(pid)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    # Find index of product in df, assuming df has 'id' column
    try:
        index = df.index[df['id'] == pid][0]
    except IndexError:
        return jsonify({"error": "Recommendation data missing 'id' column or product not found in recommendations"}), 404

    similar_titles = get_similar_products(index)

    # You can retrieve full product details from the DB using the titles, or return titles and scores directly
    recommendations = []
    for title, score in similar_titles:
        rec_product = Product.query.filter_by(title=title).first()
        if rec_product:
            recommendations.append(rec_product.to_dict())

    return jsonify({
        "selected_product": product.to_dict(),
        "recommendations": recommendations
    }), 200
