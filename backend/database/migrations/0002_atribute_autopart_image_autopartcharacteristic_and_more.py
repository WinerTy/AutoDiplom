# Generated by Django 5.1.4 on 2024-12-05 13:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Atribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название')),
                ('description', models.TextField(blank=True, max_length=1024, null=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Атрибут',
                'verbose_name_plural': 'Атрибуты',
            },
        ),
        migrations.CreateModel(
            name='AutoPart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название')),
                ('description', models.TextField(max_length=1024, verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('count', models.PositiveIntegerField(default=0, verbose_name='Количество')),
            ],
            options={
                'verbose_name': 'Автозапчасть',
                'verbose_name_plural': 'Автозапчасти',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображения',
            },
        ),
        migrations.CreateModel(
            name='AutoPartCharacteristic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=256, verbose_name='Значение')),
                ('atribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.atribute', verbose_name='Атрибут')),
                ('auto_part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.autopart', verbose_name='Автозапчасть')),
            ],
            options={
                'verbose_name': 'Характеристика автозапчасти',
                'verbose_name_plural': 'Характеристики автозапчастей',
            },
        ),
        migrations.AddField(
            model_name='autopart',
            name='images',
            field=models.ManyToManyField(to='database.image', verbose_name='Изображения'),
        ),
    ]
