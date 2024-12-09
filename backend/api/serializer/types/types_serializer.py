from rest_framework import serializers


from database.models import Types


class TypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Types
        fields = ["id", "name"]
