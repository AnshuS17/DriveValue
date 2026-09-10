# 🚗 DriveValue — AI Used Car Price Predictor & Camera Scanner

[![Live Demo](https://img.shields.io/badge/Live%20Demo-drivevalue--five.vercel.app-111111?style=for-the-badge&logo=vercel)](https://drivevalue-five.vercel.app/predict)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)](https://scikit-learn.org)
[![MongoDB](https://img.shields.io/badge/MongoDB-4.6-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://mongodb.com)

> **"Know what your car is really worth."**  
> 🔗 **Live Web Application**: [https://drivevalue-five.vercel.app/predict](https://drivevalue-five.vercel.app/predict)

---

## 📌 Project Overview

**DriveValue** is a modern, production-grade Machine Learning & Artificial Intelligence web application designed to predict the accurate resale value of second-hand cars in the Indian automotive market.

Instead of relying on subjective dealer estimates, DriveValue utilizes a **Random Forest Regression ML pipeline** trained on 2,750+ car records across 17 major brands, coupled with an **HTML5 WebRTC Live Camera Photo Scanner** and a **Rule-Based Explanation Engine**.

---

## 🌟 Key Features

1. **📷 Live Camera Photo Valuation**: Capture a live photo of any vehicle using your camera or upload an image to receive instant visual attribute detection and price valuation.
2. **🎯 Manual Specification Estimator**: Input car brand, model, manufacturing year, kilometers driven, fuel type, transmission, ownership, and condition for exact valuation.
3. **📊 Market Valuation Range ($\pm 5.5\%$)**: Displays minimum and maximum fair market resale range.
4. **📈 Feature Importance Chart**: Visualizes key pricing drivers (Engine CC, Year, Brand, KM driven) using **Chart.js**.
5. **💡 Rule-Based Explanation Engine**: Generates natural language insights explaining key value drivers without requiring paid LLM API keys.
6. **🚗 MongoDB Used Car Catalog**: Search, filter, and view 2,750+ car records by brand, fuel type, transmission, and year.
7. **⚙️ Fail-Safe Execution**: Built with PyMongo MongoDB connection manager + local CSV fallback ensuring 100% uptime.

---

## 🛠️ Technology Stack

| Component | Technology Used |
| :--- | :--- |
| **Frontend** | HTML5, Vanilla CSS3 (Custom Monochrome Palette `#F5F5F5` / `#111111`), JavaScript (ES6+), WebRTC Camera API, Chart.js |
| **Backend Framework** | Python 3.9+, Flask Web Framework, Vercel Serverless Python Runtime |
| **Machine Learning** | Scikit-Learn, Pandas, NumPy, Joblib |
| **Database** | MongoDB (PyMongo Driver) with local CSV fallback (`data/raw/cars.csv`) |
| **Deployment** | Vercel Serverless Functions (`api/index.py` entrypoint) |

---

## 📊 Machine Learning Model Performance

We evaluated 4 supervised regression algorithms on 2,750 vehicle records:

| Algorithm | R² Score ($R^2$) | MAE (Mean Absolute Error) | RMSE (Root Mean Squared Error) | Status |
| :--- | :---: | :---: | :---: | :--- |
| **Random Forest Regressor** | **0.9597 (95.97%)** | **₹88,650** | **₹1,63,573** | **Selected Top Model** |
| Gradient Boosting Regressor | 0.9503 (95.03%) | ₹1,06,876 | ₹1,81,504 | Evaluated |
| Decision Tree Regressor | 0.9002 (90.02%) | ₹1,20,617 | ₹2,57,266 | Evaluated |
| Linear Regression | 0.8009 (80.09%) | ₹2,58,636 | ₹3,63,409 | Evaluated |

---

## 🎓 College Viva & Interview Q&A (Defense Guide)

### **Q1: What is the main objective of this project?**
> **Answer**: To replace subjective manual car appraisal with a data-driven Supervised Machine Learning model that estimates second-hand car market values based on physical specs, usage, condition, and market depreciation.

### **Q2: Which ML algorithm was selected and why?**
> **Answer**: **Random Forest Regressor**. It achieved the highest $R^2$ score (**0.9597**) and lowest MAE (**₹88,650**). Random Forest handles non-linear relationships, multi-collinearity, and categorical variables better than single Decision Trees or Linear Regression.

### **Q3: What are the primary factors affecting car price in your dataset?**
> **Answer**: Based on feature importance analysis:
> 1. **Engine Capacity (Engine CC)**: 45.2%
> 2. **Manufacturing Year (Age)**: 24.8%
> 3. **Brand & Model**: 13.5%
> 4. **Kilometers Driven**: 3.4%
> 5. **Ownership & Condition**: 4.1%

### **Q4: How does the AI Camera Scanner work?**
> **Answer**: It leverages the HTML5 WebRTC `getUserMedia()` API to stream video feed into an HTML5 Canvas. When the user snaps a photo, the image is converted into a base64 string and sent to `/api/predict-image`, where visual attribute extraction and market regression formulas compute the price.

### **Q5: How does the app handle database failure or offline mode?**
> **Answer**: `DatabaseManager` in `database/db.py` attempts a MongoDB connection with an 800ms timeout. If MongoDB is unreachable (e.g. no internet or local database down), it seamlessly switches to an in-memory CSV cache (`data/raw/cars.csv`), ensuring zero app crashes.

### **Q6: How are human-readable explanations generated without paid LLM API keys?**
> **Answer**: We built a deterministic rule-based natural language generator (`generate_price_explanation`). It checks vehicle age, mileage threshold, ownership, and condition ratings to output structured, grammatically coherent sentences explaining positive and negative price drivers.

### **Q7: How is the application deployed on Vercel?**
> **Answer**: Vercel routes incoming HTTP requests via `vercel.json` to `api/index.py`. Flask initializes explicit template and static paths, and `includeFiles` packages the required templates, datasets, and static files into a lightweight AWS Lambda container.

---

## ⚡ Quick Start Guide (Local Setup)

1. **Clone Repository & Navigate**:
   ```bash
   git clone git@github.com:AnshuS17/DriveValue.git
   cd DriveWorth
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **(Optional) Re-train ML Model**:
   ```bash
   python -m ml.train_model
   ```

4. **Run Flask Application**:
   ```bash
   python app.py
   ```

5. **Open in Browser**:
   Navigate to `http://127.0.0.1:5001` or `http://127.0.0.1:5000`

---

## 🔌 API Endpoints Summary

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `GET /` | `GET` | Home Page |
| `GET /predict` | `GET` | Vehicle Valuation & Camera Scanner Page |
| `GET /cars` | `GET` | Used Cars Catalog & Search Page |
| `GET /admin` | `GET` | Admin Portal for Listing Management |
| `GET /api/stats` | `GET` | Returns DB vehicle counts, average price & brands |
| `GET /api/brands-models` | `GET` | Brand-to-model catalog mapping for dynamic UI dropdowns |
| `GET /api/cars` | `GET` | Paginated car inventory with search & filter |
| `POST /api/predict` | `POST` | Accepts vehicle JSON parameters and returns ML prediction |
| `POST /api/predict-image` | `POST` | Accepts base64 image from camera and returns valuation |
| `GET /api/model-info` | `GET` | Returns ML evaluation metrics and feature importances |

---

## 📄 License & Credits

Developed for academic presentation & open-source demonstration.  
**Live Application**: [https://drivevalue-five.vercel.app/predict](https://drivevalue-five.vercel.app/predict)
