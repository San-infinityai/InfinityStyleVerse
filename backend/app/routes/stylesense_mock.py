from flask import Flask, jsonify, request
import random
import os
import csv
from datetime import datetime

app = Flask(__name__)

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
    try:
        data = request.get_json()

        # Basic validation
        if not data or "preference" not in data:
            return jsonify({"error": "Missing 'preference' in request body"}), 400
        
        mock_response = mock_stylesense_suggest(data["preference"])

        log_entry = {
            "user_id": data.get('user_id', 'unknown'),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "api_call": "stylesense_suggest",
            "response_type": "style_suggestion",
            "response_value": mock_response["suggestion"],
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
            "api_call": "stylesense_suggest",
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

if __name__ == '__main__':
    app.run(debug=True, port=5002)