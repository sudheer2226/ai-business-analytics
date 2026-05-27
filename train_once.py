"""
Run this ONCE before starting the app for the first time.
This trains the model on the default sales.csv dataset.

Command: python train_once.py
"""
from src.data_cleaning import load_data, clean_data, detect_column_types
from src.model_training import train_model

df = load_data("data/sales.csv")
df = clean_data(df)

numeric_cols, categorical_cols = detect_column_types(df)
print(f"Numeric columns found: {numeric_cols}")
print(f"Categorical columns found: {categorical_cols}")

# Use all numeric cols except last one as features; last one as target
feature_cols = numeric_cols[:-1]
target_col = numeric_cols[-1]

print(f"Training with features: {feature_cols} → predicting: {target_col}")

model, score, feat, tgt = train_model(df, feature_cols, target_col)
print(f"Model trained! R2 Score: {score}")
print("Saved as model.pkl")
