# Generated by Django 4.0.5 on 2022-10-04 09:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agency_site', '0002_alter_clients_tel_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clients',
            name='tel_number',
            field=models.CharField(max_length=16, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in this format +380960351321. Up to 15 digits allowed.', regex='^\\+38\\((050|063|067|093|096)\\)d{7}$')], verbose_name='Телефон'),
        ),
    ]
