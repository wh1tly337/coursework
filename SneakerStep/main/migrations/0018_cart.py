# Generated by Django 4.2.7 on 2023-11-17 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_alter_assortmentadding_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=255, verbose_name='Товар')),
                ('size', models.IntegerField(verbose_name='Размер')),
                ('price', models.IntegerField(verbose_name='Цена')),
                ('quantity', models.IntegerField(default=1, verbose_name='Количество')),
            ],
        ),
    ]