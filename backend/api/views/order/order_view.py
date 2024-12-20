from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from database.models import Order
from api.serializer.order.order_serializer import OrderSerializer
from database.exceptions import OutOfCount


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            order = serializer.instance

            response_data = {"detail": "Заказ успешно создан", "order_id": order.id}

            return Response(response_data, status=status.HTTP_201_CREATED)
        except OutOfCount as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
