import joblib
import numpy as np
from app.schemas.input_schema import BusinessInput  # если используете pydantic
import os

VECTOR_PATH = "vectorizers.joblib"
MODEL_PATH = "training/model.pkl"

# Загрузка модели и векторайзеров
if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTOR_PATH):
    raise FileNotFoundError("Не найдена модель или векторайзеры. Обучите модель сначала.")

model = joblib.load(MODEL_PATH)
vectorizers = joblib.load(VECTOR_PATH)

text_columns = ["skills", "customers", "mobility", "competitors", "problems"]

def preprocess_input(data: BusinessInput):
    # Преобразуем каждое текстовое поле через векторайзер
    vectors = []
    for col in text_columns:
        vect = vectorizers[col]
        text = getattr(data, col) or ""
        v = vect.transform([text]).toarray()
        vectors.append(v)
    # Объединяем в один вектор
    X_text = np.hstack(vectors)
    investment = np.array([[data.investment if data.investment else 0]])
    return np.hstack([investment, X_text])

def predict_success(data: BusinessInput):
    X = preprocess_input(data)
    proba = model.predict_proba(X)[0][1]
    prediction = model.predict(X)[0]
    return {
        "prediction": int(prediction),
        "probability": float(proba)
    }