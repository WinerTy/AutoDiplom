from django.contrib import admin
from django.db import models
from image_uploader_widget.widgets import ImageUploaderWidget
from .models import (
    CustomUser,
    AutoPart,
    Atribute,
    AutoPartCharacteristic,
    AutoPartImage,
    Category,
    AutoMark,
    OrderItem,
    Order,
    Types,
)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "get_total_price")
    filter_fields = ("user", "created_at")

    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
        "user__phone",
    )
    list_per_page = 100
    inlines = [OrderItemInline]

    def get_total_price(self, obj):
        price = obj.total_price
        return f"{price} ₽"

    get_total_price.short_description = "Общая стоимость"


@admin.register(AutoMark)
class AutoMarkAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_per_page = 100
    search_fields = ("name",)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "date_joined",
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_per_page = 100
    formfield_overrides = {
        models.ImageField: {"widget": ImageUploaderWidget},
    }


@admin.register(Atribute)
class AtributeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_per_page = 100
    search_fields = ("name",)


class AutoPartCharacteristicInline(admin.TabularInline):
    model = AutoPartCharacteristic
    extra = 1


class AutoPartImageInline(admin.TabularInline):
    model = AutoPartImage
    extra = 1
    formfield_overrides = {
        models.ImageField: {"widget": ImageUploaderWidget},
    }

    class Media:
        css = {
            "all": ("css/admin/InlineWidget.css",),
        }


@admin.register(AutoPart)
class AutoPartAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "get_price", "count")
    list_display_links = ("id", "name")
    search_fields = ("name", "description")
    list_per_page = 100

    inlines = [AutoPartCharacteristicInline, AutoPartImageInline]
    formfield_overrides = {
        models.ImageField: {"widget": ImageUploaderWidget},
    }

    def get_price(self, obj):
        return f"{obj.price} ₽"

    get_price.short_description = "Цена"


@admin.register(Types)
class TypesAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_per_page = 100
    search_fields = ("name",)
