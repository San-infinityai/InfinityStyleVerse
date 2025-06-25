from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import joblib

app = Flask(__name__)
CORS(app)

# Loading the model
model_path = r'C:\Users\acer\Desktop\Infinity AI Work\InfinityStyleVerse\models\esg_model.pkl'
model = joblib.load(model_path)

@app.route('/api/esg-score', methods=['POST'])
def score():
    try:
        # Getting JSON data from the request
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Validating required fields
        required_fields = ['water_use', 'carbon_emission', 'ethical_rating']
        if not all(field in data for field in required_fields):
            return jsonify({'error': f'Missing required fields: {required_fields}'}), 400

        # Converting the data to a dataframe for prediction
        input_df = pd.DataFrame([data])

        # Predicting ESG score
        score = model.predict(input_df)[0]
        return jsonify({'score': round(score, 2)})

    except ValueError as ve:
        return jsonify({'error': f'Invalid input data: {str(ve)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)