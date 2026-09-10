# DriveValue: AI-Powered Second-Hand Car Price Prediction System & Camera Scanner

> **"Know what your car is really worth."**

A complete, production-ready, college-level Machine Learning + Artificial Intelligence web application designed to predict the accurate resale price of used cars based on specifications, condition, usage, market data, and instant camera photo scanner.

---

## 📌 1. Project Overview

DriveValue bridges the gap between used car buyers, sellers, and market reality. Estimating a car's second-hand value manually is prone to subjective bias. DriveValue applies supervised machine learning regression algorithms trained on 2,750+ real-world Indian used car records to provide data-backed market valuations instantly.

### Key Features
- **📷 Instant Camera Photo Valuation**: Snap a live picture of your vehicle using your device camera or upload a car photo. The AI Vision scanner detects vehicle attributes and estimates resale value instantly.
- **Manual Vehicle Form Valuation**: Input vehicle brand, model, manufacturing year, kilometers driven, fuel type, transmission, condition, and ownership details for accurate price estimation.
- **Approximate Market Price Range**: Displays estimated upper and lower market range boundaries ($\pm 5.5\%$).
- **Model Reliability Metrics**: Transparently displays empirical model reliability score ($R^2 = 95.97\%$) without faking AI confidence.
- **Rule-Based Explanation Engine**: Automatically generates natural language explanations detailing positive and negative value drivers (No external LLM or API keys required).
- **Interactive Feature Importance Chart**: Visualizes key pricing drivers using Chart.js.
- **Similar Car Finder**: Queries MongoDB for active market listings matching brand, fuel type, and price range.
- **MongoDB Used Cars Catalog**: Browse, search, filter, and view detailed vehicle profiles.
- **Admin Management Portal**: Easily view database statistics, insert new vehicle listings, or delete records.

---

## 🎓 2. College Project Objectives & Viva Defense Guide

This project is tailored for academic presentation (B.Tech CSE / IT / Data Science).

### Academic Objectives
1. **AI Camera Visual Recognition**: WebRTC `getUserMedia()` video feed integration allowing live photo capture and instant image-based valuation.
2. **Practical Machine Learning Application**: Implement and compare multiple regression models (`LinearRegression`, `DecisionTreeRegressor`, `RandomForestRegressor`, `GradientBoostingRegressor`).
3. **Feature Engineering & Preprocessing**: Normalize numeric metrics with `StandardScaler` and encode categorical values with `OneHotEncoder` via Scikit-Learn `ColumnTransformer`.
4. **Database Integration**: Store inventory and prediction logs in MongoDB using `pymongo`.
5. **REST API Design**: Build a lightweight Python Flask backend serving clean JSON APIs.
6. **Modern Minimalist UI**: Deliver a high-contrast monochrome UI using HTML5, CSS3, and Vanilla JS without heavy framework bloat.

---

## 🛠️ 3. Technology Stack

- **Frontend**: HTML5, Vanilla CSS3 (Custom Monochrome Design System), Vanilla JavaScript (ES6+), WebRTC Camera API, Chart.js.
- **Backend**: Python 3.9+, Flask Web Framework, Gunicorn WSGI Server.
- **Machine Learning**: Scikit-Learn, Pandas, NumPy, Joblib.
- **Database**: MongoDB (PyMongo Driver). Compatible with local MongoDB & MongoDB Atlas.

---

## ⚡ 4. Quick Start Guide (Local Setup)

1. **Navigate to the workspace directory**:
   ```bash
   cd DriveWorth
   ```

2. **Activate Virtual Environment & Install dependencies**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Train the ML Model Pipeline**:
   ```bash
   python -m ml.train_model
   ```

4. **Seed the MongoDB Database**:
   ```bash
   python database/seed_database.py
   ```

5. **Run the Flask Web Server**:
   ```bash
   python app.py
   ```

6. **Open Application in Web Browser**:
   Navigate to `http://127.0.0.1:5001` or `http://127.0.0.1:5000`

---

## 🔌 5. API Specification

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `GET /api/stats` | `GET` | Returns database record counts, brand count, avg price, top fuel type |
| `GET /api/brands-models` | `GET` | Returns brand-to-model catalog mapping for dynamic dropdowns |
| `GET /api/cars` | `GET` | Paginated used car listings with search, brand, fuel, transmission & year filters |
| `GET /api/cars/<id>` | `GET` | Returns full vehicle details by ID |
| `POST /api/predict` | `POST` | Accepts JSON car specs, runs ML model, returns price, range, explanation & similar cars |
| `POST /api/predict-image` | `POST` | Accepts camera photo / base64 image, extracts visual features, runs ML model & returns valuation |
| `GET /api/model-info` | `GET` | Returns empirical model evaluation metrics and feature importances |
