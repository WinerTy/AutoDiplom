from rest_framework import serializers

from database.models import AutoPart


class AutoPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoPart
        fields = (
            "id",
            "name",
            "description",
            "count",
            "price",
        )
