# Generated by Django 4.0.5 on 2022-10-04 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agency_site', '0010_alter_clients_tel_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clients',
            name='tel_number',
            field=models.CharField(max_length=15, unique=True, verbose_name='Телефон'),
        ),
    ]
