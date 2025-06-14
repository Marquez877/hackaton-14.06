from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def train_model(data):
    """Обучает ML-модель на основе данных."""
    # Выберите признаки и целевую переменную
    X = data[['investment', 'skills', 'mobility']]  # Признаки
    y = data['success']  # Целевая переменная (добавьте её в данные заранее)

    # Разделение данных
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Обучение модели
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Оценка модели
    y_pred = model.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred)}")

    return model