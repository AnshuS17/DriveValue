import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split

NUMERICAL_FEATURES = ["year", "km_driven", "engine_cc", "mileage", "seats"]
CATEGORICAL_FEATURES = ["brand", "model", "fuel_type", "transmission", "ownership", "location", "condition"]
BOOLEAN_FEATURES = ["insurance_valid"]

def load_data(filepath="data/raw/cars.csv"):
    """
    Loads raw CSV data and handles basic type conversions.
    """
    df = pd.read_csv(filepath)
    df["insurance_valid"] = df["insurance_valid"].astype(int)
    return df

def get_preprocessor():
    """
    Creates a scikit-learn ColumnTransformer for scaling numerical features
    and one-hot encoding categorical features.
    """
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERICAL_FEATURES),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL_FEATURES),
            ("bool", "passthrough", BOOLEAN_FEATURES)
        ],
        remainder="drop"
    )
    return preprocessor

def prepare_data(filepath="data/raw/cars.csv", test_size=0.2, random_state=42):
    """
    Loads dataset, splits into X and y, and performs train_test_split.
    """
    df = load_data(filepath)
    
    feature_cols = NUMERICAL_FEATURES + CATEGORICAL_FEATURES + BOOLEAN_FEATURES
    X = df[feature_cols]
    y = df["price"]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    return X_train, X_test, y_train, y_test, feature_cols
