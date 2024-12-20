from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializer.user.user_serializer import UserRegisterSerializer

from database.models import CustomUser
from rest_framework.permissions import AllowAny


class UserRegisterView(APIView):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Пользователь успешно зарегистрирован"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
