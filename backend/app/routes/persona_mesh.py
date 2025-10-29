from flask import Blueprint, jsonify, request

persona_mesh_bp = Blueprint("persona_mesh", __name__)
mock_embeddings = {
    "User1": {"style": "casual", "vector": [0.1, 0.2, 0.3]},
    "User2": {"style": "trendy", "vector": [0.4, 0.5, 0.6]},
    "User3": {"style": "versatile", "vector": [0.7, 0.8, 0.9]}
}

def mock_personamesh_recommendation(user_id):
    """
    Mock PersonaMesh recommendation function.
    Returns recommendation & confidence score based on mock style embeddings.
    """
    embedding_data = mock_embeddings.get(user_id, {"style": "generic", "vector": [0.0, 0.0, 0.0]})
    style = embedding_data["style"]
    recommendations = {
        "casual": {"recommendation": "Casual blue t-shirt", "confidence": 0.9},
        "trendy": {"recommendation": "Trendy leather jacket", "confidence": 0.85},
        "versatile": {"recommendation": "Versatile black jeans", "confidence": 0.8},
        "generic": {"recommendation": "Explore new styles", "confidence": 0.7}
    }
    return recommendations.get(style, recommendations["generic"])

@persona_mesh_bp.route('/api/personamesh/recommend', methods=['POST'])
def recommend():
    data = request.get_json() or {}
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({"error": "Missing 'user_id' in request"}), 400

    result = mock_personamesh_recommendation(user_id)
    return jsonify(result)
