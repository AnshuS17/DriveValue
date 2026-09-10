import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from ml.preprocess import prepare_data

def evaluate_saved_model(model_path="model/car_price_model.pkl"):
    """
    Evaluates the currently saved model pipeline against the test dataset
    and prints detailed performance metrics.
    """
    if not os.path.exists(model_path):
        print(f"Error: Saved model file '{model_path}' not found. Please train the model first.")
        return None

    print(f"Loading trained model from '{model_path}'...")
    pipeline = joblib.load(model_path)
    
    _, X_test, _, y_test, _ = prepare_data()
    
    y_pred = pipeline.predict(X_test)
    
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    print("\n================ MODEL EVALUATION SUMMARY ================")
    print(f"R² Score (Coefficient of Determination) : {r2:.4f}")
    print(f"Mean Absolute Error (MAE)              : ₹{mae:,.2f}")
    print(f"Root Mean Squared Error (RMSE)          : ₹{rmse:,.2f}")
    print("==========================================================")
    
    return {
        "r2": round(float(r2), 4),
        "mae": round(float(mae), 2),
        "rmse": round(float(rmse), 2)
    }

if __name__ == "__main__":
    evaluate_saved_model()
