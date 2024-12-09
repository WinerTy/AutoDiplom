from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters
from api.serializer.auto_part.auto_part_serializer import AutoPartSerializer
from api.filter import AutoPartFilter
from database.models import AutoPart
from backend.core.pagination import LargeResultsSetPagination


class AutoPartViewSet(ModelViewSet):
    queryset = AutoPart.objects.order_by("id")
    serializer_class = AutoPartSerializer
    filterset_class = AutoPartFilter
    filter_backends = (filters.DjangoFilterBackend,)
    http_method_names = ["get", "options"]
    pagination_class = LargeResultsSetPagination
