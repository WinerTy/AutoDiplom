from django_filters import rest_framework as filters


from database.models import Types


class TypesFilter(filters.FilterSet):
    class Meta:
        model = Types
        fields = ["obj_type"]
