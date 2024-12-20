from rest_framework.viewsets import ModelViewSet

from database.models import AutoMark
from api.serializer.auto_mark.auto_mark_serializer import AutoMarkSerializer


class AutoMarkView(ModelViewSet):
    queryset = AutoMark.objects.order_by("name")
    serializer_class = AutoMarkSerializer
