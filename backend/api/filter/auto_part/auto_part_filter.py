from django_filters import rest_framework as filters

from database.models import AutoPart, Category, AutoMark


class AutoPartFilter(filters.FilterSet):
    category = filters.ModelMultipleChoiceFilter(
        field_name="category", queryset=Category.objects.all()
    )
    price = filters.NumberFilter(field_name="price", lookup_expr="lt")
    mark = filters.ModelMultipleChoiceFilter(
        field_name="mark", queryset=AutoMark.objects.all()
    )

    class Meta:
        model = AutoPart
        fields = ["mark", "price", "category"]
