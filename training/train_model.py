import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
import os

# Пути для сохранения
VECTOR_PATH = "vectorizers.joblib"
MODEL_PATH = "training/model.pkl"

# Загружаем данные
df = pd.read_csv("businesses.csv")

# Проверяем наличие колонки success
if "success" not in df.columns:
    raise Exception("В CSV отсутствует колонка 'success'!")

text_columns = ["skills", "customers", "mobility", "competitors", "problems"]
vectorizers = {}

# Обучаем и сохраняем TF-IDF векторайзеры для каждой текстовой колонки
for col in text_columns:
    vectorizer = TfidfVectorizer()
    vectorizer.fit(df[col].fillna(""))
    vectorizers[col] = vectorizer

joblib.dump(vectorizers, VECTOR_PATH)
print(f"Vectorizers saved to {VECTOR_PATH}")

# Функция преобразования текстов в векторы
def transform_text_columns(df, vectorizers):
    vectors = []
    for col in text_columns:
        vect = vectorizers[col]
        v = vect.transform(df[col].fillna("")).toarray()
        vectors.append(v)
    return np.hstack(vectors)

# Преобразуем текстовые признаки
X_text = transform_text_columns(df, vectorizers)

# Добавляем числовой признак инвестиции
investment = df["investment"].fillna(0).values.reshape(-1, 1)

# Объединяем в итоговый массив
X = np.hstack([investment, X_text])

# Целевая переменная
y = df["success"].values

# Разбиваем на обучение и тест
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Обучаем модель
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Оцениваем качество
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Test accuracy: {acc:.4f}")

# Сохраняем модель
os.makedirs("training", exist_ok=True)
joblib.dump(model, MODEL_PATH)
print(f"Model saved to {MODEL_PATH}")