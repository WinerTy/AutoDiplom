# Generated by Django 5.1.4 on 2024-12-05 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0005_category_autopart_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='categories/', verbose_name='Изображение'),
        ),
    ]
