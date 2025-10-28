import pandas as pd
import numpy as np
import os

np.random.seed(42)
N_SAMPLES = 200 

data = {
    'sku': [f'SKU{i:04d}' for i in range(N_SAMPLES)],
    'image_uri': [f's3://styleverse/raw/img_{i}.jpg' for i in range(N_SAMPLES)],
    'category': np.random.choice(['top', 'bottom', 'outerwear', 'shoe'], N_SAMPLES),
    'aesthetic_score_label': np.round(np.random.uniform(0.5, 1.0, N_SAMPLES), 2),
    'color': np.random.choice(['black', 'white', 'navy', 'red', 'neon'], N_SAMPLES),
    'pattern': np.random.choice(['solid', 'striped', 'floral'], N_SAMPLES),
    'occasion_label': np.random.choice(['party', 'casual', 'formal', 'streetwear'], N_SAMPLES),
}

df_seed = pd.DataFrame(data)

data_dir = 'backend/app/StyleSense/data'
os.makedirs(data_dir, exist_ok=True)

df_seed.to_csv(f'{data_dir}/stylesense_seed_data.csv', index=False)
print(f"Saved seed dataset to {data_dir}/stylesense_seed_data.csv")
print(f"Dataset size: {len(df_seed)} samples.")