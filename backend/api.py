from flask import Flask, request, jsonify
from backend.data_processing import load_and_clean_data
from backend.model import train_model

app = Flask(__name__)

# Загрузка и обучение модели
data = load_and_clean_data('data/opros.csv')
model = train_model(data)

@app.route('/predict', methods=['POST'])
def predict():
    """Эндпоинт для предсказаний."""
    data = request.get_json()
    features = [data['feature1'], data['feature2'], data['feature3']]
    prediction = model.predict([features])
    return jsonify({'prediction': int(prediction[0])})

if __name__ == '__main__':
    app.run(debug=True)