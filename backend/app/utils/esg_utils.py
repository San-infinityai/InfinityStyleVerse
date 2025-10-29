import numpy as np
import pandas as pd
import joblib
import os

MODEL_PATH = os.path.join('models', 'esg_model.pkl')

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    print(f"ESG model could not be loaded: {e}")
    model = None

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

def generate_esg_columns(df, seed=42):
    np.random.seed(seed)  

    def generate_values(row):
        material = str(row['material']).lower().strip()

        if 'tencel' in material:
            water_use = np.random.uniform(4000000, 5000000)
            carbon_emission = np.random.uniform(1, 5)
            ethical_rating = np.random.randint(3, 5)
        elif 'vegan leather' in material:
            water_use = np.random.uniform(1500000, 2500000)
            carbon_emission = np.random.uniform(100, 350)
            ethical_rating = np.random.randint(2, 5)
        elif 'bamboo' in material:
            water_use = np.random.uniform(800000, 2000000)
            carbon_emission = np.random.uniform(150, 420)
            ethical_rating = np.random.randint(2, 5)
        elif 'recycled' in material or 'organic' in material:
            water_use = np.random.uniform(200000, 700000)
            carbon_emission = np.random.uniform(50, 150)
            ethical_rating = np.random.randint(4, 6)
        else:
            water_use = np.random.uniform(800000, 2500000)
            carbon_emission = np.random.uniform(100, 300)
            ethical_rating = np.random.randint(2, 5)

        return pd.Series([round(water_use, 2), round(carbon_emission, 2), ethical_rating])

    df[['water_use', 'carbon_emission', 'ethical_rating']] = df.apply(generate_values, axis=1)
    return df

def get_esg_badge(score):
    if score >= 80:
        return '🟢'
    elif score >= 50:
        return '🟡'
    return '🔴'

def compute_esg_score(df, model):
    features = df[['water_use', 'carbon_emission', 'ethical_rating']].fillna(0)
    df['esg_score'] = model.predict(features)

    #Category-specific weighting
    def adjust_score(row):
        material = str(row.get('material', '')).lower().strip()
        score = row['esg_score']

        if 'leather' in material and 'vegan' not in material:
            score -= 15
        elif 'polyester' in material:
            score -= 10
        elif 'organic cotton' in material:
            score += 10
        elif 'bamboo' in material:
            score += 8
        elif 'recycled' in material:
            score += 12

        return score

    df['esg_score'] = df.apply(adjust_score, axis=1)

    # Validation: ensure ESG score is between 0 and 100
    if (df['esg_score'] < 0).any() or (df['esg_score'] > 100).any():
        print("Warning: Some ESG scores fall outside the expected range (0–100). Clipping them.")
        df['esg_score'] = df['esg_score'].clip(lower=0, upper=100)
    
    # Add ESG badge column
    df['esg_badge'] = df['esg_score'].apply(get_esg_badge)

    return df

