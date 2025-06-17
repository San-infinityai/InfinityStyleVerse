from flask import Flask, jsonify, request
from flask_cors import CORS
from transformers import pipeline
import re

app = Flask(__name__)
CORS(app) 

generator = pipeline("text-generation", model="gpt2")

def format_ai_output(response):

    cleaned = re.sub(r'[^\w\s\'.,!?]', '', response) 
    sentences = re.split(r'[.!?]+', cleaned) 
    complete_sentences = []
    for s in sentences:
        s = s.strip()
        if s: 
            end_pos = cleaned.index(s) + len(s)
            if end_pos < len(cleaned) and cleaned[end_pos] in ['.', '!', '?']:
                complete_sentences.append(s + cleaned[end_pos])
    if complete_sentences:
        return ' '.join(complete_sentences).strip() + '.'
    else:
        return cleaned

@app.route('/api/style-advice', methods=['POST'])  
def style_advice():
    try:
        prompt = request.json.get('question')
        if not prompt:
            return jsonify({"error": "No question provided"}), 400

        full_prompt = f"You are a helpful AI fashion stylist. {prompt}"
        result = generator(full_prompt, max_new_tokens=80, truncation=True)
        formatted_advice = format_ai_output(result[0]['generated_text'])
        return jsonify({"advice": formatted_advice})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)