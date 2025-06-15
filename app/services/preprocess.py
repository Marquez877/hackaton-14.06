from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
import joblib
import os

# Общие векторайзеры (заранее обучить!)
vectorizers = {
    "skills": TfidfVectorizer(),
    "customers": TfidfVectorizer(),
    "mobility": TfidfVectorizer(),
    "competitors": TfidfVectorizer(),
    "problems": TfidfVectorizer(),
}

VECTOR_PATH = "vectorizers.joblib"

def save_vectorizers():
    joblib.dump(vectorizers, VECTOR_PATH)

def load_vectorizers():
    global vectorizers
    if os.path.exists(VECTOR_PATH):
        vectorizers = joblib.load(VECTOR_PATH)

def preprocess_input(data):
    def split_and_count(field):
        if not field:
            return []
        return [x.strip() for x in field.split(",") if x.strip()]

    # Получаем списки для каждого текстового поля
    skills_list = split_and_count(data.skills)
    customers_list = split_and_count(data.customers)
    mobility_list = split_and_count(data.mobility)
    competitors_list = split_and_count(data.competitors)
    problems_list = split_and_count(data.problems)

    # Преобразуем списки обратно в строки для vectorizer
    skills_str = " ".join(skills_list)
    customers_str = " ".join(customers_list)
    mobility_str = " ".join(mobility_list)
    competitors_str = " ".join(competitors_list)
    problems_str = " ".join(problems_list)

    # Векторизация
    features_text = [
        skills_str,
        customers_str,
        mobility_str,
        competitors_str,
        problems_str,
    ]

    # Трансформируем каждое поле в вектор
    vectors = []
    for key, vect in vectorizers.items():
        vect_vector = vect.transform([features_text[list(vectorizers.keys()).index(key)]]).toarray()
        vectors.append(vect_vector)

    # Объединяем все векторы по горизонтали
    text_features = np.hstack(vectors)

    # Числовой признак инвестиции
    investment_feature = np.array([[data.investment if data.investment is not None else 0]])

    # Итоговый массив
    result = np.hstack([investment_feature, text_features])

    return result

def vectorize(df):
    # Если векторайзеры уже обучены, загрузим их
    if os.path.exists(VECTOR_PATH):
        load_vectorizers()
        all_features = []
        for key, vect in vectorizers.items():
            transformed = vect.transform(df[key].fillna("")).toarray()
            all_features.append(transformed)
        return pd.DataFrame(np.hstack(all_features))
    else:
        # Обучаем векторайзеры на данных и сохраняем
        for key, vect in vectorizers.items():
            vect.fit(df[key].fillna(""))
        save_vectorizers()
        all_features = []
        for key, vect in vectorizers.items():
            transformed = vect.transform(df[key].fillna("")).toarray()
            all_features.append(transformed)
        return pd.DataFrame(np.hstack(all_features))