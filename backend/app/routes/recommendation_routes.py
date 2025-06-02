from flask import Flask, jsonify
import pickle

app = Flask(__name__)

with open(r'C:\Users\acer\Desktop\Infinity AI Work\InfinityStyleVerse\models\recommender_model.pkl', 'rb') as f:
    model_data = pickle.load(f)
    df = model_data['df']
    similarities = model_data['similarities']

def get_similar_products(index):
    scores = list(enumerate(similarities[index]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    top_3 = scores[1:4]
    return [(df['title'][i], score) for i, score in top_3]

# Define the API route
@app.route('/api/recommend/<int:pid>')
def recommend(pid):
    if pid < 0 or pid >= len(df):
        return jsonify({"error": "Invalid product ID"}), 400
    similar = get_similar_products(pid)
    return jsonify({"similar": similar})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
