from flask import Flask, jsonify, request
import random

app = Flask(__name__)

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

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 