# Generated by Django 4.2.7 on 2023-11-14 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_alter_assortmentadding_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='final_price',
            field=models.IntegerField(blank=True, null=True, verbose_name='Сумма заказа'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата обновления заказа'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='payment_method',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Способ оплаты'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='status',
            field=models.CharField(choices=[('Decorated', 'Оформлен'), ('Sent', 'Отправлен'), ('Completed', 'Завершен'), ('Cancelled', 'Отменен'), ('Refund', 'Возврат')], default='Оформлен', max_length=10, verbose_name='Статус заказа'),
        ),
    ]
