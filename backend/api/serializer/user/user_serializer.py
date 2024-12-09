from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from database.models import CustomUser


class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ("email", "password1", "password2")

    def validate_passwords(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError({"detail": "Пароли не совпадают"})
        return data

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Аккаунт с такой почтой уже существует")
        return value

    def validate(self, attrs):
        attrs = super().validate(attrs)
        self.validate_passwords(attrs)
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data["email"],
        )
        user.set_password(validated_data["password1"])
        user.save()
        return user
