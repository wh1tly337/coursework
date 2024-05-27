# Generated by Django 5.0.3 on 2024-03-12 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_alter_users_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='users',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.RemoveField(
            model_name='users',
            name='items_id',
        ),
        migrations.AddField(
            model_name='cart',
            name='user_id',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='ID пользователя'),
        ),
    ]