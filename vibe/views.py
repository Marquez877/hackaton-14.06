from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RequestSerializer
from .models import Request

class AnalyzeView(APIView):
    def post(self, request):
        serializer = RequestSerializer(data=request.data)
        if serializer.is_valid():
# Сохраняем сообщение (если нужно сохранять в БД)
            # instance = serializer.save()
            message = serializer.validated_data['message'].lower()  

        # Простейшая rule-based логика
            if "дизайн" in message and "принтер" in message:  
                idea = "Бизнес по производству 3D-сувениров"  
                score = "высокая"  
            elif "репетитор" in message or "обучение" in message:  
                idea = "Онлайн-обучение или курсы"  
                score = "средняя"  
            elif "продукты" in message or "еда" in message:  
                idea = "Маленькое кафе или доставка еды"  
                score = "высокая"  
            else:  
                idea = "Начните с фриланса или онлайн-бизнеса"  
                score = "низкая"

            return Response({  
            "result": f"Рекомендуем: {idea}. Вероятность успеха: {score}."  
        }, status=status.HTTP_200_OK)  
        else:  
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)