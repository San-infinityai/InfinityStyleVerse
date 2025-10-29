import pickle
import json
import numpy as np
import os
import time
from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest

MODEL_PATH = 'models/intent_classifier_mvp.pkl' 
INTERNAL_PORT = 5001 
INTENT_MODEL_ARTIFACT = None
LABEL_ENCODER_CLASSES = None

def load_model_artifact():
    global INTENT_MODEL_ARTIFACT, LABEL_ENCODER_CLASSES
    try:
        with open(MODEL_PATH, 'rb') as f:
            artifact = pickle.load(f)
            INTENT_MODEL_ARTIFACT = artifact['pipeline']
            LABEL_ENCODER_CLASSES = artifact['label_encoder_classes']
        print(f"Model loaded successfully from {MODEL_PATH}")
        print(f"Model classes: {list(LABEL_ENCODER_CLASSES)}")
    except FileNotFoundError:
        print(f"ERROR: Model file not found at {MODEL_PATH}")
    except Exception as e:
        print(f"ERROR loading model: {e}")


def get_intent_and_confidence(text_input):
    if INTENT_MODEL_ARTIFACT is None:
        raise RuntimeError("Intent model is not loaded.")
        
    probas = INTENT_MODEL_ARTIFACT.predict_proba([text_input])[0]
    
    max_proba_index = np.argmax(probas)
    confidence = probas[max_proba_index]
    
    predicted_intent = LABEL_ENCODER_CLASSES[max_proba_index]
    
    return predicted_intent, confidence

# Flask App Setup 
app = Flask(__name__)
load_model_artifact() 

@app.route('/predict_intent', methods=['POST'])
def predict_intent_endpoint():
    if not request.is_json:
        return jsonify({"error": "Missing JSON payload"}), 400
    
    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({"error": "Missing 'prompt' field in request"}), 400
    
    if INTENT_MODEL_ARTIFACT is None:
        return jsonify({"error": "Model unavailable. Service starting up."}), 503

    try:
        start_time = time.perf_counter()
        intent, confidence = get_intent_and_confidence(prompt)
        end_time = time.perf_counter()
        
        latency_ms = (end_time - start_time) * 1000

        return jsonify({
            "intent": intent, 
            "confidence": round(confidence, 4),
            "latency_ms": round(latency_ms, 3)
        })
        
    except Exception as e:
        return jsonify({"error": f"Internal inference error: {e}"}), 500

if __name__ == '__main__':
    print(f"NeuroCoreOS Intent Microservice running on port {INTERNAL_PORT}...")
    app.run(host='0.0.0.0', port=INTERNAL_PORT, debug=True, use_reloader=False)