# Generated by Django 4.0.5 on 2022-10-17 06:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agency_site', '0018_alter_orders_client_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typeoforder',
            name='price',
            field=models.IntegerField(default=1000, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Цена'),
        ),
    ]
