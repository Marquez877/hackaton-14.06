from flask import Flask, request, jsonify
from backend.data_processing import load_and_clean_data
from backend.model import train_model

app = Flask(__name__)

# Загрузка и обучение модели
file_path = 'data/opros.csv'
data = load_and_clean_data(file_path)
model = train_model(data)

@app.route('/predict', methods=['POST'])
def predict():
    """Эндпоинт для предсказаний."""
    data = request.get_json()
    features = [data['investment']]
    prediction = model.predict([features])
    return jsonify({'prediction': int(prediction[0])})

if __name__ == '__main__':
    app.run(debug=True)