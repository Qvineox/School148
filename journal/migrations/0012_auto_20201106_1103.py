# Generated by Django 3.1.1 on 2020-11-06 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0011_auto_20201106_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disciples',
            name='scheme',
            field=models.CharField(default='empty', max_length=20, verbose_name='Цветовая схема'),
        ),
    ]
