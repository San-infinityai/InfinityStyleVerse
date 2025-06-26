from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import joblib

app = Flask(__name__)
CORS(app)

# Loading the model
model_path = r'C:\Users\acer\Desktop\Infinity AI Work\InfinityStyleVerse\models\esg_model.pkl'
model = joblib.load(model_path)

def suggest_alternative(material):
  
    material = material.lower().strip()  
    alternatives = {
        'polyester': 'organic cotton',  # Lower carbon and water use
        'cotton': 'recycled cotton',    # Reduces water use compared to conventional cotton
        'nylon': 'recycled nylon',      # Lower carbon footprint
        'acrylic': 'bamboo fabric',     # Renewable and biodegradable
        'leather': 'vegan leather'      # Animal-friendly alternative
    }
    return alternatives.get(material, 'recycled nylon')  # Recycled nylon if not found

@app.route('/api/esg-score', methods=['POST'])
def score():
    try:
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Validating required fields
        required_fields = ['water_use', 'carbon_emission', 'ethical_rating']
        if not all(field in data for field in required_fields):
            return jsonify({'error': f'Missing required fields: {required_fields}'}), 400

        # Checking for material
        material = data.get('material', '').lower().strip()

        # Converting to dataframe and filter to model features
        input_df = pd.DataFrame([data])[[ 'water_use', 'carbon_emission', 'ethical_rating']]

        # Predicting ESG score
        score = model.predict(input_df)[0]

        # Suggesting alternative material
        alternative = suggest_alternative(material) if material else None

        # Response
        response = {'score': round(score, 2)}
        if alternative:
            response['sustainable_alternative'] = alternative

        return jsonify(response)

    except ValueError as ve:
        return jsonify({'error': f'Invalid input data: {str(ve)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)