from rest_framework import serializers
from database.models import Order, OrderItem, AutoPart, Types
from database.exceptions import OutOfCount


class OrderItemSerializer(serializers.ModelSerializer):
    auto_part_id = serializers.PrimaryKeyRelatedField(
        queryset=AutoPart.objects.all(), source="auto_part"
    )

    class Meta:
        model = OrderItem
        fields = ["auto_part_id", "count"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    payment_type = serializers.PrimaryKeyRelatedField(
        queryset=Types.objects.filter(obj_type="payment")
    )
    delivery_type = serializers.PrimaryKeyRelatedField(
        queryset=Types.objects.filter(obj_type="delivery")
    )

    class Meta:
        model = Order
        fields = [
            "user",
            "payment_type",
            "delivery_type",
            "delivery_address",
            "items",
        ]
        extra_kwargs = {
            "user": {"read_only": True},
        }

    def validate(self, data):
        delivery_type = data.get("delivery_type")
        delivery_type_name = Types.objects.get(id=delivery_type.id).name
        if delivery_type_name.lower() != "самовывоз":
            delivery_address = data.get("delivery_address")
            if not delivery_address:
                raise serializers.ValidationError(
                    {"delivery_address": "Поле обязательно для заполнения"}
                )

        return data

    def validate_items(self, items):
        for item in items:
            auto_part = item["auto_part"]
            requested_count = item["count"]

            if requested_count < 1:
                raise serializers.ValidationError(
                    {"detail": "Количество товара должно быть больше 0"}
                )

            if auto_part.count < requested_count:
                raise serializers.ValidationError(
                    {
                        "detail": f"Недостаточно товара '{auto_part.name}' на складе. Доступно: {auto_part.count}, запрошено: {requested_count}"
                    }
                )
        return items

    def create_order(self, validated_data):
        """
        Создает объект Order на основе валидированных данных.
        """
        return Order.objects.create(**validated_data)

    def create_order_items(self, order, items_data):
        """
        Создает объекты OrderItem и связывает их с заказом.
        Также проверяет и уменьшает количество товара на складе.
        """
        for item_data in items_data:
            auto_part = item_data["auto_part"]
            count = item_data["count"]

            # Проверяем и уменьшаем количество товара на складе
            try:
                auto_part.decrease_count(count)
            except OutOfCount as e:
                raise serializers.ValidationError({"detail": str(e)})

            # Создаем позицию заказа
            OrderItem.objects.create(order=order, **item_data)

    def create(self, validated_data):
        """
        Создает заказ и позиции заказа.
        """
        items_data = validated_data.pop("items")
        order = self.create_order(validated_data)
        self.create_order_items(order, items_data)
        return order
