import numpy as np
import pandas as pd

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

def compute_esg_score(df, model):
    features = df[['water_use', 'carbon_emission', 'ethical_rating']].fillna(0)
    df['esg_score'] = model.predict(features)

    # Validation: ensure ESG score is between 0 and 100
    if (df['esg_score'] < 0).any() or (df['esg_score'] > 100).any():
        print("Warning: Some ESG scores fall outside the expected range (0–100). Clipping them.")
        df['esg_score'] = df['esg_score'].clip(lower=0, upper=100)

    return df
