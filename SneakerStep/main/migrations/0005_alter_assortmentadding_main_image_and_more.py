# Generated by Django 4.2.7 on 2023-11-07 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_assortmentadding_sizes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assortmentadding',
            name='main_image',
            field=models.ImageField(upload_to='static/main/images_new/assortment/<django.db.models.fields.AutoField>', verbose_name='Главное изображение'),
        ),
        migrations.AlterField(
            model_name='assortmentadding',
            name='second_image',
            field=models.ImageField(upload_to='static/main/images_new/assortment/<django.db.models.fields.AutoField>', verbose_name='Втророе изображение'),
        ),
        migrations.AlterField(
            model_name='assortmentadding',
            name='third_image',
            field=models.ImageField(upload_to='static/main/images_new/assortment/<django.db.models.fields.AutoField>', verbose_name='Третье изображение'),
        ),
    ]