from fastapi import FastAPI
from typing import Dict, Any
from app.schemas.input_schema import BusinessInput
from app.models.predictor import predict_success
from app.models.recommender import recommend_alternative
from app.utils.logger import logger

app = FastAPI()

@app.post("/predict/", summary="Predict business success and return AI recommendation", description="Returns success probability and recommendations.")
def predict(data: BusinessInput) -> Dict[str, Any]:
    """
    Эндпоинт для предсказания успеха бизнеса.
    Если вероятность успеха ниже 0.6, возвращает альтернативные рекомендации.
    """
    try:
        result = predict_success(data)
        success = result['probability'] >= 0.6
        response = {
            "success": success,
            "probability": round(result["probability"], 3),
            "recommendation": recommend_alternative(data) if not success else None
        }
        return response
    except Exception as e:
        logger.exception("Prediction failed")
        return {"error": str(e)}