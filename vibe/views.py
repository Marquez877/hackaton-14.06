from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Функция для чтения файла с бизнес-данными
def load_successful_businesses(filepath='successful_businesses.txt'):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = f.read()
        return data
    except Exception as e:
        return ""

class AnalyzeView(APIView):
    def post(self, request):
        user_message = request.data.get("message", "").strip()
        if not user_message:
            return Response({"error": "Поле 'message' обязательно"}, status=400)

        businesses_info = load_successful_businesses()
        if not businesses_info:
            return Response({"error": "Не удалось загрузить информацию о бизнесах"}, status=500)

        prompt = f"""
Ты — опытный бизнес-аналитик из Бишкека.
Ниже список локальных успешных бизнесов:

{businesses_info}

Пользователь описал свои возможности:
"{user_message}"

На основе этого предложи бизнес-идею, подходящую для него, и оцени шансы на успех.
Формат ответа:
- Идея
- Почему она подходит
- Оценка вероятности успеха (низкая / средняя / высокая)
-Актуальность в Кыргызстане
-Потенциальные риски
-Возможные траты в сомах
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
