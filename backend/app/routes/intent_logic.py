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

# Dummy function that simulates IntentLogic intent prediction returning intent scores
def mock_intentlogic(user_action):
    
    intent_scores = {
        "buy_shoes": round(random.uniform(0.7, 0.9), 2),
        "buy_accessory": round(random.uniform(0.6, 0.8), 2),
        "explore_more": round(random.uniform(0.5, 0.7), 2)
    }
    return {"user_action": user_action, "intent_scores": intent_scores}


@app.route('/api/intentlogic', methods=['POST'])
def intentlogic():
    try:
        data = request.get_json()
        user_action = data.get('user_action', 'default_action')

        result = mock_intentlogic(user_action)

        log_entry = {
            "user_id": data.get('user_id', 'unknown'),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "api_call": "intentlogic",
            "response_type": "intent_scores",
            "response_value": str(result["intent_scores"]),
            "confidence": "N/A",  # IntentLogic uses scores, not confidence
            "request_data": str(data)
        }

        logs.append(log_entry)

        fieldnames = ["user_id", "timestamp", "api_call", "response_type", "response_value", "confidence", "request_data"]
        with open(log_file, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if os.stat(log_file).st_size == 0:
                writer.writeheader()
            writer.writerow(log_entry)

        return jsonify(result)
    except Exception as e:
        error_entry = {
            "user_id": data.get('user_id', 'unknown'),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "api_call": "intentlogic",
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
    app.run(debug=True, host='0.0.0.0', port=5001) 