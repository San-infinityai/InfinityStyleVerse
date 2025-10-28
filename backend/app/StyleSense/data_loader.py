import pandas as pd
from typing import Literal

DATA_PATH = 'backend/app/StyleSense/data/stylesense_seed_data.csv'

def load_stylesense_data(
    module: Literal["catalog_vision", "outfit_scorer", "bodymorph"]
) -> pd.DataFrame:
    try:
        df = pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        raise FileNotFoundError(f"FATAL: Data file not found at {DATA_PATH}.")

    if module == "catalog_vision":
        return df[['sku', 'image_uri', 'category', 'color', 'pattern']]

    elif module == "outfit_scorer":
        return df[['sku', 'aesthetic_score_label', 'occasion_label', 'image_uri']]
    
    elif module == "bodymorph":
        return df[['sku', 'image_uri']] 
    
    else:
        raise ValueError(f"Unknown module: {module}")

def validate_and_clean(df: pd.DataFrame) -> pd.DataFrame:
    df.dropna(subset=['image_uri'], inplace=True)
    if 'aesthetic_score_label' in df.columns:
        df = df[(df['aesthetic_score_label'] >= 0) & (df['aesthetic_score_label'] <= 1)]
    return df

if __name__ == '__main__':
    df_catalog = load_stylesense_data("catalog_vision")
    df_catalog = validate_and_clean(df_catalog)
    print(f"\n Loaded {len(df_catalog)} samples for Catalog Vision. ETL skeleton operational.")