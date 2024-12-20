from django.db import models, transaction
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from database.utils.manager.user_manager import CustomUserManager
from database.exceptions import OutOfCount


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        max_length=255,
        blank=False,
    )

    # All these field declarations are copied as-is
    # from `AbstractUser`
    first_name = models.CharField(
        "Имя",
        max_length=30,
        blank=True,
    )
    last_name = models.CharField(
        "Фамилия",
        max_length=150,
        blank=True,
    )
    is_staff = models.BooleanField(
        "Статус персонала",
        default=False,
        help_text="Для доступа в административную часть сайта.",
    )
    is_active = models.BooleanField(
        "Активный",
        default=True,
        help_text="Обозначает, должен ли этот пользователь "
        "рассматриваться как активный. Снимите этот флажок вместо "
        "удаления учетных записей.",
    )
    date_joined = models.DateTimeField(
        "Дата регистрации",
        default=timezone.now,
    )
    phone = models.CharField(
        max_length=21, verbose_name="Номер телефона", blank=True, null=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name="Название")
    image = models.ImageField(
        upload_to="categories/", verbose_name="Изображение", blank=True, null=True
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class AutoMark(models.Model):
    name = models.CharField(max_length=256, verbose_name="Название", unique=True)

    class Meta:
        verbose_name = "Марка"
        verbose_name_plural = "Марки"

    def __str__(self):
        return self.name


class AutoPart(models.Model):
    name = models.CharField(max_length=256, verbose_name="Название")
    mark = models.ForeignKey(AutoMark, on_delete=models.CASCADE, verbose_name="Марка")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Категория"
    )
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    count = models.PositiveIntegerField(default=0, verbose_name="Количество")
    image = models.ImageField(
        upload_to="images/", verbose_name="Изображение", blank=True, null=True
    )

    class Meta:
        verbose_name = "Автозапчасть"
        verbose_name_plural = "Автозапчасти"

    def __str__(self):
        return self.name

    def decrease_count(self, count: int = 1):
        if self.count <= count:
            raise OutOfCount("Недостаточно товара на складе", self.name, self.count)
        self.count -= count
        self.save()

    def check_count(self, count: int = 1):
        if self.count < count:
            raise OutOfCount("Недостаточно товара на складе", self.name, self.count)


class Atribute(models.Model):
    name = models.CharField(max_length=256, verbose_name="Название")
    description = models.TextField(
        max_length=1024, verbose_name="Описание", blank=True, null=True
    )

    class Meta:
        verbose_name = "Атрибут"
        verbose_name_plural = "Атрибуты"

    def __str__(self):
        return self.name


class AutoPartCharacteristic(models.Model):
    auto_part = models.ForeignKey(
        AutoPart, on_delete=models.CASCADE, verbose_name="Автозапчасть"
    )
    atribute = models.ForeignKey(
        Atribute, on_delete=models.CASCADE, verbose_name="Атрибут"
    )
    value = models.CharField(max_length=256, verbose_name="Значение")

    class Meta:
        verbose_name = "Характеристика"
        verbose_name_plural = "Характеристики"

    def __str__(self):
        return f"{self.auto_part.name} - {self.atribute.name}"


class AutoPartImage(models.Model):
    auto_part = models.ForeignKey(
        AutoPart, on_delete=models.CASCADE, verbose_name="Автозапчасть"
    )
    image = models.ImageField(upload_to="images/", verbose_name="Изображение")

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

    def __str__(self):
        return f"{self.auto_part.name} - {self.image.url}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        "Order", on_delete=models.CASCADE, verbose_name="Заказ", related_name="items"
    )
    auto_part = models.ForeignKey(
        AutoPart, on_delete=models.CASCADE, verbose_name="Автозапчасть"
    )
    count = models.PositiveIntegerField(default=1, verbose_name="Количество")

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

    def __str__(self):
        return f"{self.auto_part.name} - {self.count}"

    def get_total_price(self):
        return self.auto_part.price * self.count

    def clean(self, *args, **kwargs):
        if self.count > self.auto_part.count:
            raise ValidationError("Недостаточно товара в наличии")

    @transaction.atomic
    def save(self, *args, **kwargs):
        if not self.pk:
            self.auto_part.decrease_count(self.count)
        self.order.total_price += self.get_total_price()
        self.order.save()
        super().save(*args, **kwargs)


class Types(models.Model):
    name = models.CharField(max_length=256, verbose_name="Название")
    obj_type = models.CharField(
        max_length=256,
        verbose_name="Тип объекта",
        choices=[("delivery", "Доставка"), ("payment", "Платеж")],
    )

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"


class Order(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    payment_type = models.ForeignKey(
        Types,
        on_delete=models.CASCADE,
        verbose_name="Тип оплаты",
        related_name="payment_type",
    )
    is_paid = models.BooleanField(default=False, verbose_name="Оплачен")

    delivery_type = models.ForeignKey(
        Types,
        on_delete=models.CASCADE,
        verbose_name="Тип доставки",
        related_name="delivery_type",
    )
    delivery_address = models.CharField(
        max_length=256, verbose_name="Адрес", blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Общая стоимость", default=0
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    # def save(self, *args, **kwargs):
    #     if self.delivery_type.name.lower() == "cамовывоз":
    #         self.delivery_address = "Пунк выдачи"

    #     super().save(*args, **kwargs)
