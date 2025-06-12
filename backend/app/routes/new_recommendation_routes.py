from flask import Flask, jsonify, request
import pickle
import numpy as np

app = Flask(__name__)

with open(r'C:\Users\acer\Desktop\Infinity AI Work\InfinityStyleVerse\models\new_recommender_model.pkl', 'rb') as f:
    model_data = pickle.load(f)
    df = model_data['df']
    combined_similarities = model_data['similarities']

def get_similar_products(index):
    scores = list(enumerate(combined_similarities[index]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    top_3 = scores[1:4]
    return [(df['product_id'][i], df['title'][i], score, df['image_url'][i]) for i, score in top_3]

def find_product_index_by_id(product_id):
    product_id = str(product_id).strip()
    df['product_id'] = df['product_id'].astype(str).str.strip()
    if product_id in df['product_id'].values:
        return df.index[df['product_id'] == product_id].tolist()[0]
    else:
        raise ValueError(f"Product ID {product_id} not found")

@app.route('/api/recommend-by-id', methods=['POST'])
def recommend_by_id():
    try:
        data = request.json
        if not data or 'product_id' not in data:
            return jsonify({"error": "No product_id provided"}), 400
        
        product_id = data['product_id']
        product_index = find_product_index_by_id(product_id)
        
        similar = get_similar_products(product_index)
        response = {"similar": [{"product_id": pid, "title": title, "score": float(score), "image_url": image_url} for pid, title, score, image_url in similar]}
        return jsonify(response)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)