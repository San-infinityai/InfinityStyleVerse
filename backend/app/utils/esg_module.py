import joblib
import os
import pandas as pd

model_path = os.path.join('models', 'esg_model.pkl')
model = joblib.load(model_path)

def assign_esg_badge(score):
    if score >= 75:
        return 'High'
    elif score >= 50:
        return 'Moderate'
    else:
        return 'Low'

def compute_esg_score(data):
    input_df = pd.DataFrame([data])[['water_use', 'carbon_emission', 'ethical_rating']]
    score = float(model.predict(input_df)[0])
    return round(score, 2)

def suggest_alternative(material):
    if not material:
        return None
    material = material.lower().strip()
    alternatives = {
        'polyester': 'organic cotton',
        'cotton': 'recycled cotton',
        'nylon': 'recycled nylon',
        'acrylic': 'bamboo fabric',
        'leather': 'vegan leather'
    }
    sustainable_options = set(alternatives.values())  
    if material in sustainable_options:
        return "The provided material is a sustainable material."
    return alternatives.get(material, 'recycled nylon')

# Final ESG pipeline
def process_product_esg(product_json):
    score = compute_esg_score(product_json)
    badge = assign_esg_badge(score)
    suggestion = suggest_alternative(product_json.get('material', ''))

    return {
        'score': score, 
        'badge': badge,
        'sustainable_alternative': suggestion
    }

