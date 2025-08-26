from flask import Flask, jsonify, request
import random
import os
import csv
from datetime import datetime

app = Flask(__name__)

<<<<<<< HEAD
=======
log_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'logs', 'infinitybrain_logs.csv'))
if not os.path.exists(os.path.dirname(log_file)):
    os.makedirs(os.path.dirname(log_file))

# Loading existing logs or initializing empty list with a proper structure
try:
    with open(log_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        logs = [dict(row) for row in reader]  
except FileNotFoundError:
    logs = []

>>>>>>> ef030e382c61d85b6655a2ed69f924d9ffc1c9c7
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
    try:
        data = request.get_json()

<<<<<<< HEAD
    if not data or "image" not in data:
        return jsonify({"error": "Missing 'image' in request body"}), 400
=======
        if not data or "image" not in data:
            return jsonify({"error": "Missing 'image' in request body"}), 400
        
        mock_response = mock_visionaryai_analyze(data["image"])
>>>>>>> ef030e382c61d85b6655a2ed69f924d9ffc1c9c7

        log_entry = {
            "user_id": data.get('user_id', 'unknown'),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "api_call": "visionaryai_analyze",
            "response_type": "analysis",
            "response_value": f"{mock_response['material']}, {mock_response['color']}",
            "confidence": str(mock_response["confidence"]),
            "request_data": str(data)
        }
        logs.append(log_entry)

        fieldnames = ["user_id", "timestamp", "api_call", "response_type", "response_value", "confidence", "request_data"]
        with open(log_file, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if os.stat(log_file).st_size == 0:
                writer.writeheader()
            writer.writerow(log_entry)

        return jsonify(mock_response)
    except Exception as e:
        error_entry = {
            "user_id": data.get('user_id', 'unknown'),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "api_call": "visionaryai_analyze",
            "response_type": "error",
            "response_value": str(e),
            "confidence": "N/A",
            "request_data": str(data)
        }
        logs.append(error_entry)

        with open(log_file, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(error_entry)
        return jsonify({"error": str(e)}), 500

@app.route('/api/visionaryai/infer', methods=['POST'])
def infer_image():
    try:
        data = request.get_json()

        if not data or "image" not in data:
            return jsonify({"error": "Missing 'image' in request body"}), 400
        
        mock_response = mock_visionaryai_infer(data["image"])

        log_entry = {
            "user_id": data.get('user_id', 'unknown'),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "api_call": "visionaryai_infer",
            "response_type": "inference",
            "response_value": str(mock_response["image_urls"]),
            "confidence": str(mock_response["confidence"]),
            "request_data": str(data)
        }
        logs.append(log_entry)

        fieldnames = ["user_id", "timestamp", "api_call", "response_type", "response_value", "confidence", "request_data"]
        with open(log_file, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if os.stat(log_file).st_size == 0:
                writer.writeheader()
            writer.writerow(log_entry)

        return jsonify(mock_response)
    except Exception as e:
        error_entry = {
            "user_id": data.get('user_id', 'unknown'),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "api_call": "visionaryai_infer",
            "response_type": "error",
            "response_value": str(e),
            "confidence": "N/A",
            "request_data": str(data)
        }
        logs.append(error_entry)
        
        with open(log_file, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(error_entry)
        return jsonify({"error": str(e)}), 500

@app.route('/api/visionaryai/infer', methods=['POST'])
def infer_image():
    data = request.get_json()

    if not data or "image" not in data:
        return jsonify({"error": "Missing 'image' in request body"}), 400

    mock_response = mock_visionaryai_infer(data["image"])
    return jsonify(mock_response)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
