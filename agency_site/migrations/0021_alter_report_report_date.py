# Generated by Django 4.0.5 on 2022-10-17 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agency_site', '0020_alter_assistant_comments_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='report_date',
            field=models.DateField(auto_now_add=True, verbose_name='Дата создания'),
        ),
    ]
