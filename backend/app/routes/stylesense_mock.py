from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# Mock StyleSense function
def mock_stylesense_suggest(user_preferences):
    suggestions = [
        "Pair with white sneakers",
        "Try a leather jacket",
        "Accessorize with a silver necklace",
        "Layer with a light cardigan",
        "Match with a denim skirt"
    ]
    return {
        "suggestion": random.choice(suggestions),
        "confidence": 0.85
    }

@app.route('/api/stylesense/suggest', methods=['POST'])
def suggest_style():
    data = request.get_json()

    # Basic validation
    if not data or "preference" not in data:
        return jsonify({"error": "Missing 'preference' in request body"}), 400

    mock_response = mock_stylesense_suggest(data["preference"])
    return jsonify(mock_response)

if __name__ == '__main__':
    app.run(debug=True, port=5002)