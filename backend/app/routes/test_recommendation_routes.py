from flask import Flask, jsonify, request
from flask_cors import CORS
import pickle
import csv
import os
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import random

# Setting up Flask app
app = Flask(__name__)
CORS(app)

# Loading the saved model data
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'models', 'new_recommender_model.pkl')
with open(MODEL_PATH, 'rb') as f:
    model_data = pickle.load(f)
    df = model_data['df']
    combined_similarities = model_data['similarities']

df['product_id'] = df['product_id'].astype(str).str.strip()

df['combined_text'] = df['title'] + " " + df['descriptions']

# Recompute TF-IDF only which is needed to process new user text input
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['combined_text'])

# Log file setup
log_file = os.path.join(os.path.dirname(__file__), '..' ,'..', '..', 'data', 'logs', 'recommendation_log.csv')
os.makedirs(os.path.dirname(log_file), exist_ok=True)
if not os.path.exists(log_file):
    with open(log_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'product_id', 'title', 'action', 'input'])

# Log function
def log_event(product_id, title, action, user_input):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, product_id, title, action, user_input])

# Recommend products
@app.route('/api/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()
        user_input = data.get('query', '').strip().lower()

        if not user_input:
            return jsonify({"error": "No input provided"}), 400

        # Convert user input to TF-IDF vector
        user_vector = tfidf.transform([user_input])
        text_scores = cosine_similarity(user_vector, tfidf_matrix).flatten()

        category_scores = np.max(combined_similarities, axis=1)
        color_scores = np.max(combined_similarities, axis=1)

        # Combine weighted scores
        weight_text = 0.6
        weight_category = 0.2
        weight_color = 0.2

        combined_scores = (
            weight_text * text_scores +
            weight_category * category_scores +
            weight_color * color_scores
        )

        # Get top 3
        scores_with_indices = sorted(enumerate(combined_scores), key=lambda x: x[1], reverse=True)
        top_3 = scores_with_indices[:3]

        recommendations = []
        for i, score in top_3:
            product = {
                'product_id': df.loc[i, 'product_id'],
                'title': df.loc[i, 'title'],
                'description': df.loc[i, 'descriptions'],
                'category': df.loc[i, 'category'],
                'color': df.loc[i, 'color'],
                'image_url': df.loc[i, 'image_url'],
                'score': float(score)
            }
            log_event(product['product_id'], product['title'], 'shown', user_input)
            recommendations.append(product)

        # fallback process
        if max(score for _, score in top_3) < 0.1:
            recommendations = []
            fallback_indices = random.sample(range(len(df)), 3)
            for i in fallback_indices:
                product = {
                    'product_id': df.loc[i, 'product_id'],
                    'title': df.loc[i, 'title'],
                    'description': df.loc[i, 'descriptions'],
                    'category': df.loc[i, 'category'],
                    'color': df.loc[i, 'color'],
                    'image_url': df.loc[i, 'image_url'],
                    'score': 0.0
                }
                log_event(product['product_id'], product['title'], 'shown', user_input)
                recommendations.append(product)

        return jsonify({"results": recommendations})

    except Exception as e:
        print("Error in /api/recommend:", e)
        return jsonify({"error": str(e)}), 500

# Log event
@app.route('/api/log-click', methods=['POST'])
def log_click():
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        title = data.get('title')
        user_input = data.get('input', '')
        if not product_id or not title:
            return jsonify({"error": "Missing product_id or title"}), 400

        log_event(product_id, title, 'clicked', user_input)
        return jsonify({"message": "Click logged"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)