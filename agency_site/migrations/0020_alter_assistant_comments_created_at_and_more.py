# Generated by Django 4.0.5 on 2022-10-17 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agency_site', '0019_alter_typeoforder_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assistant_comments',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='status',
            field=models.CharField(choices=[('Closed', 'Закрыта'), ('In process', 'На рассмотрении менеджера'), ('Pending client', 'На рассмотрении клиента'), ('Payed', 'Оплачена'), ('Rejected by client', 'Отклонена клиентом'), ('Rejected by manager', 'Отклонена менеджером'), ('In work', 'В работе')], default='In process', max_length=50, verbose_name='Статус заказа'),
        ),
    ]
