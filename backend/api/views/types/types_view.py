from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters
from api.serializer.types.types_serializer import TypesSerializer
from database.models import Types
from api.filter import TypesFilter


class TypesViewSet(ModelViewSet):
    queryset = Types.objects.all()
    serializer_class = TypesSerializer
    http_method_names = ["get", "options"]
    allowed_methods = ["get", "options"]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = TypesFilter
