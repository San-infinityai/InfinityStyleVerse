from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# Dummy function for InfinityBrain prediction

def mock_infinitybrain_predict(prompt):
    trends = ["High demand for blue dresses", "Rise in sustainable jackets", "Popular neon tops"]
    confidence = round(random.uniform(0.8, 0.95), 2) 
    return {"trend_forecast": random.choice(trends), "confidence": confidence}

@app.route('/api/infinitybrain/predict', methods=['POST'])
def predict():
    # JSON request
    data = request.get_json()
    prompt = data.get('prompt', 'Default prompt')
    
    # Calling the function and returning the result
    prediction = mock_infinitybrain_predict(prompt)
    return jsonify(prediction)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)