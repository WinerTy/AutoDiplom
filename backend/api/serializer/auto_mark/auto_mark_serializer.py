from rest_framework import serializers

from database.models import AutoMark


class AutoMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoMark
        fields = ["id", "name"]
