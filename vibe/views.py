from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SUCCESSFUL_BUSINESSES = """
1. Кофейня возле университета с бюджетом 5000 сом, успех высокий.
2. Instagram-магазин с корейской косметикой, ведёт молодая девушка, успех высокий.
3. Услуги по ремонту телефонов рядом с кампусом, бюджет 3000 сом, успех средний.
4. Онлайн-курсы по программированию через Telegram и Zoom, успех высокий.
5. Мобильная прачечная по району с доставкой через WhatsApp, успех средний.
"""

class AnalyzeView(APIView):
    def post(self, request):
        user_message = request.data.get("message", "").strip()
        if not user_message:
            return Response({"error": "Поле 'message' обязательно"}, status=400)

        prompt = f"""
Ты — опытный бизнес-аналитик из Бишкека.
Ниже список локальных успешных бизнесов:

{SUCCESSFUL_BUSINESSES}

Пользователь описал свои возможности:
"{user_message}"

На основе этого предложи бизнес-идею, подходящую для него, и оцени шансы на успех.
Формат ответа:
- Идея
- Почему она подходит
- Оценка вероятности успеха (низкая / средняя / высокая)
"""

        try:
            chat_completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Ты бизнес-консультант, анализируешь идеи стартапов для начинающих."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            reply = chat_completion.choices[0].message.content.strip()
            return Response({"result": reply})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
