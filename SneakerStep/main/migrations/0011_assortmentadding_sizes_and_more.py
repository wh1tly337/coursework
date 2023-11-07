# Generated by Django 4.2.7 on 2023-11-07 11:57

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_orders_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='assortmentadding',
            name='sizes',
            field=models.CharField(default='36 37 38 39 40 41 42 43 44 45', max_length=50, verbose_name='Размеры'),
        ),
        migrations.AlterField(
            model_name='assortmentadding',
            name='main_image',
            field=models.ImageField(upload_to=main.models.user_directory_path, verbose_name='Главное изображение'),
        ),
        migrations.AlterField(
            model_name='assortmentadding',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='assortmentadding',
            name='second_image',
            field=models.ImageField(upload_to=main.models.user_directory_path, verbose_name='Втророе изображение'),
        ),
        migrations.AlterField(
            model_name='assortmentadding',
            name='third_image',
            field=models.ImageField(upload_to=main.models.user_directory_path, verbose_name='Третье изображение'),
        ),
    ]