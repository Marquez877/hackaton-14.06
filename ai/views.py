import openai
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os

openai.api_key = os.getenv("OPENAI_API_KEY") # храните ключ в .env

SUCCESSFUL_BUSINESSES = """

Кофейня в центре города рядом с офисами. Бюджет: 5000$. Успех: высокий.

Магазин корейской косметики через Instagram. Успех: высокий.

Мобильная прачечная с доставкой. Бюджет: 2000$. Успех: средний.

Услуги по ремонту смартфонов возле кампусов. Успех: высокий.

Онлайн-курсы по дизайну. Успех: средне-высокий.

Мастерская 3D-печати. Успех: средний.
"""

class AnalyzeView(APIView):
    def post(self, request):
        user_message = request.data.get("message")

        if not user_message:
            return Response({"error": "Нет данных"}, status=400)

        prompt = f" "