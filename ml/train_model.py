import os
import json
import joblib
import numpy as np
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

from ml.preprocess import prepare_data, get_preprocessor, NUMERICAL_FEATURES, CATEGORICAL_FEATURES, BOOLEAN_FEATURES

def train_and_evaluate_models():
    """
    Trains multiple regression models, compares evaluation metrics, saves the best model
    pipeline along with metrics and feature importance.
    """
    os.makedirs("model", exist_ok=True)
    
    print("Loading and splitting dataset...")
    X_train, X_test, y_train, y_test, feature_cols = prepare_data()
    
    # Candidate regression models
    candidate_models = {
        "Linear Regression": LinearRegression(),
        "Decision Tree Regressor": DecisionTreeRegressor(random_state=42, max_depth=15),
        "Random Forest Regressor": RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
        "Gradient Boosting Regressor": GradientBoostingRegressor(n_estimators=100, random_state=42, learning_rate=0.1)
    }
    
    model_results = {}
    best_model_name = None
    best_r2 = -float("inf")
    best_pipeline = None
    best_metrics = {}

    print("\n--- Model Training & Comparison ---")
    for name, regressor in candidate_models.items():
        preprocessor = get_preprocessor()
        pipeline = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("regressor", regressor)
        ])
        
        # Fit pipeline
        pipeline.fit(X_train, y_train)
        
        # Predict on test set
        y_pred = pipeline.predict(X_test)
        
        # Evaluation metrics
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        print(f"Model: {name}")
        print(f"  R² Score: {r2:.4f}")
        print(f"  MAE: ₹{mae:,.2f}")
        print(f"  RMSE: ₹{rmse:,.2f}\n")
        
        model_results[name] = {
            "r2": round(float(r2), 4),
            "mae": round(float(mae), 2),
            "rmse": round(float(rmse), 2)
        }
        
        if r2 > best_r2:
            best_r2 = r2
            best_model_name = name
            best_pipeline = pipeline
            best_metrics = model_results[name]

    print(f"--> Best Model Selected: '{best_model_name}' with R² = {best_r2:.4f}")

    # Extract feature importances if available
    regressor = best_pipeline.named_steps["regressor"]
    preprocessor = best_pipeline.named_steps["preprocessor"]
    
    # Get encoded feature names
    try:
        cat_encoder = preprocessor.named_transformers_["cat"]
        encoded_cat_cols = list(cat_encoder.get_feature_names_out(CATEGORICAL_FEATURES))
    except Exception:
        encoded_cat_cols = CATEGORICAL_FEATURES
        
    all_feature_names = NUMERICAL_FEATURES + encoded_cat_cols + BOOLEAN_FEATURES

    feature_importances = []
    if hasattr(regressor, "feature_importances_"):
        importances = regressor.feature_importances_
        # Group importances back into top high-level features for UI display
        top_importances = {}
        for feat, imp in zip(all_feature_names, importances):
            # Find base feature name
            base_feat = feat.split("_")[0] if "_" in feat and feat.split("_")[0] in CATEGORICAL_FEATURES else feat
            top_importances[base_feat] = top_importances.get(base_feat, 0.0) + float(imp)
            
        sorted_feats = sorted(top_importances.items(), key=lambda x: x[1], reverse=True)
        feature_importances = [{"feature": k.replace("_", " ").title(), "importance": round(v * 100, 2)} for k, v in sorted_feats]
    else:
        # Fallback uniform weights
        feature_importances = [{"feature": col.replace("_", " ").title(), "importance": round(100.0 / len(feature_cols), 2)} for col in feature_cols]

    # Save model artifacts
    model_path = "model/car_price_model.pkl"
    columns_path = "model/model_columns.pkl"
    metrics_path = "model/metrics.json"
    importances_path = "model/feature_importances.json"
    
    joblib.dump(best_pipeline, model_path)
    joblib.dump(feature_cols, columns_path)
    
    metrics_data = {
        "best_model": best_model_name,
        "metrics": best_metrics,
        "comparison": model_results,
        "dataset_size": len(X_train) + len(X_test)
    }
    
    with open(metrics_path, "w") as f:
        json.dump(metrics_data, f, indent=4)
        
    with open(importances_path, "w") as f:
        json.dump(feature_importances, f, indent=4)

    print(f"Pipeline saved to '{model_path}'")
    print(f"Columns saved to '{columns_path}'")
    print(f"Metrics saved to '{metrics_path}'")
    print(f"Feature Importances saved to '{importances_path}'")
    
    return best_pipeline, metrics_data

if __name__ == "__main__":
    train_and_evaluate_models()
