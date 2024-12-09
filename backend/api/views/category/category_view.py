from rest_framework.viewsets import ModelViewSet


from database.models import Category
from api.serializer.category.category_serializer import CategorySerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.order_by("name")
    serializer_class = CategorySerializer
    allowed_methods = ["get", "options"]
    http_method_names = ["get", "options"]
