from flask import Flask, jsonify, request
from flask_cors import CORS
from transformers import pipeline

app = Flask(__name__)
CORS(app) 

generator = pipeline("text-generation", model="gpt2")

@app.route('/api/style-advice', methods=['POST'])
def style_advice():
    try:
        prompt = request.json.get('question')
        if not prompt:
            return jsonify({"error": "No question provided"}), 400

        result = generator(prompt, max_new_tokens=80, truncation=True)
        return jsonify({"advice": result[0]['generated_text']})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
