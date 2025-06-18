from flask import Flask, jsonify, request
from flask_cors import CORS
from transformers import pipeline
import re

app = Flask(__name__)
CORS(app) 

generator = pipeline("text-generation", model="gpt2")

# Dictionary with emojis
clothing_emojis = {
    'jacket': '🧥',
    'coat': '🧥',
    'dress': '👗',
    'trouser': '👖',
    'shirt': '👕',
    'top': '👚',
    'shoes': '👡',
    'scarf': '🧣',
    'tie': '👔',
    'short': '🩳',  # Base for shorts
    'gloves': '🧤',
    'swimsuit': '🩱',
    'hat': '👒',
    'cap': '🧢',
    'beanie': '🧢',
    'necklace': '📿',
    'sunglasses': '🕶️'
}

# Function to format the AI output with emojis
def format_ai_output(response):
    cleaned = re.sub(r'[^\w\s\'.,!?]', '', response)
    sentences = re.split(r'[.!?]+', cleaned)
    complete_sentences = []
    for s in sentences:
        s = s.strip()
        if s:  # Non-empty sentence
            # Check if the original response ends this sentence with valid punctuation
            end_pos = cleaned.index(s) + len(s)
            original_end = cleaned[end_pos] if end_pos < len(cleaned) else ''
            if original_end in ['.', '!', '?']:
                sentence = s + original_end
                # Adding emojis based on clothing keywords
                words = s.lower().split()
                for i, word in enumerate(words):
                    for clothing_type, emoji in clothing_emojis.items():
                        # Handling plural
                        if word == clothing_type or (word.endswith('s') and clothing_type in word[:-1] and clothing_type not in ['shoes', 'gloves']):
                            original_words = s.split()
                            original_word = original_words[i]
                            if emoji not in original_word:
                                sentence = sentence.replace(original_word, f"{original_word} {emoji}")
                complete_sentences.append(sentence)
    # Join back with the last punctuation
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