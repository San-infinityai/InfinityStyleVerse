from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# Mock VisionaryAI analyze function
def mock_visionaryai_analyze(image_input):
    return {
        "material": random.choice(["cotton", "silk", "denim"]),
        "color": random.choice(["blue", "red", "black"]),
        "confidence": round(random.uniform(0.75, 0.95), 2)
    }

# Mock VisionaryAI infer function (Day 5 task)
def mock_visionaryai_infer(image_input):
    sample_urls = [
        "https://example.com/images/dress1.jpg",
        "https://example.com/images/dress2.jpg",
        "https://example.com/images/dress3.jpg"
    ]
    return {
        "image_urls": sample_urls,
        "confidence": round(random.uniform(0.8, 0.95), 2)
    }

@app.route('/api/visionaryai/analyze', methods=['POST'])
def analyze_image():
    data = request.get_json()

    if not data or "image" not in data:
        return jsonify({"error": "Missing 'image' in request body"}), 400

    mock_response = mock_visionaryai_analyze(data["image"])
    return jsonify(mock_response)

@app.route('/api/visionaryai/infer', methods=['POST'])
def infer_image():
    data = request.get_json()

    if not data or "image" not in data:
        return jsonify({"error": "Missing 'image' in request body"}), 400

    mock_response = mock_visionaryai_infer(data["image"])
    return jsonify(mock_response)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
