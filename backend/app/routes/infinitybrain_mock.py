from flask import Flask, jsonify, request
from datetime import datetime
import csv
import os
import random
import numpy as np


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


# Generating mock embeddings
def generate_mock_embedding(user_id, role):
    base_vector = np.random.rand(10)  
    if role == "Admin":
        base_vector += np.random.rand(10) * 0.3  
    elif role == "Executive":
        base_vector += np.random.rand(10) * 0.1  
    return base_vector.tolist()  

# Dummy user data
dummy_users = [
    {"user_id": "user1", "role": "User"},
    {"user_id": "user2", "role": "User"},
    {"user_id": "admin1", "role": "Admin"},
    {"user_id": "exec1", "role": "Executive"}
]

# Generating embeddings for each user
user_embeddings = {user["user_id"]: generate_mock_embedding(user["user_id"], user["role"]) for user in dummy_users}

# Mock PersonaMesh recommendation function
def mock_personamesh_recommend_with_embedding(user_id):

    embedding = user_embeddings.get(user_id, generate_mock_embedding(user_id, "User"))  # Getting the embedding for the user
    base_recommendation = {
        "user1": {"recommendation": "Casual blue t-shirt", "confidence": 0.9},
        "user2": {"recommendation": "Trendy leather jacket", "confidence": 0.85},
        "admin1": {"recommendation": "Premium suit", "confidence": 0.95},
        "exec1": {"recommendation": "Elegant dress", "confidence": 0.88}
    }.get(user_id, {"recommendation": "Explore new styles", "confidence": 0.7})

    confidence_adjust = sum(embedding) / 10  # Average embedding value
    adjusted_confidence = min(0.95, max(0.7, base_recommendation["confidence"] + (confidence_adjust - 0.5) * 0.1))
    base_recommendation["confidence"] = round(adjusted_confidence, 2)
    return base_recommendation


# Dummy function for InfinityBrain prediction
def mock_infinitybrain_predict(prompt):
    trends = ["High demand for blue dresses", "Rise in sustainable jackets", "Popular neon tops"]
    confidence = round(random.uniform(0.8, 0.95), 2)
    return {"trend_forecast": random.choice(trends), "confidence": confidence}


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
            "confidence": str(prediction["confidence"]),  # Convert to string to match CSV
            "request_data": str(data)
        }

        # Appending a new log entry
        logs.append(log_entry)

        fieldnames = ["user_id", "timestamp", "api_call", "response_type", "response_value", "confidence", "request_data"]
        with open(log_file, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if os.stat(log_file).st_size == 0:
                writer.writeheader()
            writer.writerow(log_entry)

        return jsonify(prediction)
    except Exception as e:
        error_entry = {
            "user_id": user_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "api_call": "predict",
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

@app.route('/api/personamesh/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'unknown')

        recommendation = mock_personamesh_recommend_with_embedding(user_id)

        log_entry = {
            "user_id": user_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "api_call": "recommend",
            "response_type": "recommendation",
            "response_value": recommendation["recommendation"],
            "confidence": str(recommendation["confidence"]),
            "request_data": str(data)
        }
        logs.append(log_entry)

        fieldnames = ["user_id", "timestamp", "api_call", "response_type", "response_value", "confidence", "request_data"]
        with open(log_file, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if os.stat(log_file).st_size == 0:
                writer.writeheader()
            writer.writerow(log_entry)

        return jsonify(recommendation)
    except Exception as e:
        error_entry = {
            "user_id": user_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "api_call": "recommend",
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

# Placeholder health check endpoint    
@app.route('/api/health', methods=['GET'])
def health_check():
    """Placeholder health check for AI services (Day 4 task)."""
    return jsonify({
        "status": "healthy",
        "message": "AI services are running (mock)",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

# Mock EcoSense endpoint
@app.route('/api/ecosense', methods=['POST'])
def ecosense():
    try:
        # Get JSON request
        data = request.get_json()
        product_id = data.get('product_id', 'unknown_product')

        # Generate mock eco-scores
        carbon_score = round(random.uniform(2.0, 10.0), 1)  # kg CO2e
        water_usage = round(random.uniform(50.0, 200.0), 1)  # liters
        recyclability = round(random.uniform(0.5, 0.9), 2)   # percentage (0-1)

        # Return JSON response
        response = {
            "product_id": product_id,
            "carbon_score": carbon_score,
            "water_usage": water_usage,
            "recyclability": recyclability
        }

        log_entry = {
            "user_id": "N/A",  # EcoSense may not require user_id
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "api_call": "ecosense",
            "response_type": "eco_score",
            "response_value": str(response),
            "confidence": "N/A",
            "request_data": str(data)
        }

        logs.append(log_entry)

        fieldnames = ["user_id", "timestamp", "api_call", "response_type", "response_value", "confidence", "request_data"]
        with open(log_file, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if os.stat(log_file).st_size == 0:
                writer.writeheader()
            writer.writerow(log_entry)

        return jsonify(response)
    except Exception as e:
        error_entry = {
            "user_id": "N/A",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "api_call": "ecosense",
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
    app.run(debug=True, host='0.0.0.0', port=5000)