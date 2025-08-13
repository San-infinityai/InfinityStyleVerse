from flask import Flask, jsonify, request
from datetime import datetime
import csv
import os
import random


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


# Dummy function for InfinityBrain prediction
def mock_infinitybrain_predict(prompt):
    trends = ["High demand for blue dresses", "Rise in sustainable jackets", "Popular neon tops"]
    confidence = round(random.uniform(0.8, 0.95), 2)
    return {"trend_forecast": random.choice(trends), "confidence": confidence}


# Dummy function for PersonaMesh recommendation
def mock_personamesh_recommend(user_id):
    if user_id == "user1":
        return {"recommendation": "Casual blue t-shirt", "confidence": 0.9}
    elif user_id == "user2":
        return {"recommendation": "Trendy leather jacket", "confidence": 0.85}
    else:
        return {"recommendation": "Explore new styles", "confidence": 0.7}
    

@app.route('/api/infinitybrain/predict', methods=['POST'])
def predict():
    try:
        # Get JSON request
        data = request.get_json()
        prompt = data.get('prompt', 'Default prompt')
        user_id = data.get('user_id', 'unknown')

        # Calling the mock function
        prediction = mock_infinitybrain_predict(prompt)

        # Creating a log entry
        log_entry = {
            "user_id": user_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "api_call": "predict",
            "response_type": "trend_forecast",
            "response_value": prediction["trend_forecast"],
            "confidence": str(prediction["confidence"])  # Convert to string to match CSV
        }

        # Appending a new log entry
        logs.append(log_entry)

        fieldnames = ["user_id", "timestamp", "api_call", "response_type", "response_value", "confidence"]
        with open(log_file, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if os.stat(log_file).st_size == 0:
                writer.writeheader()
            writer.writerow(log_entry)

        return jsonify(prediction)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/personamesh/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'unknown')

        recommendation = mock_personamesh_recommend(user_id)

        log_entry = {
            "user_id": user_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "api_call": "recommend",
            "response_type": "recommendation",
            "response_value": recommendation["recommendation"],
            "confidence": str(recommendation["confidence"])  
        }

        logs.append(log_entry)

        fieldnames = ["user_id", "timestamp", "api_call", "response_type", "response_value", "confidence"]
        with open(log_file, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if os.stat(log_file).st_size == 0:
                writer.writeheader()
            writer.writerow(log_entry)

        return jsonify(recommendation)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)