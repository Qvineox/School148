# Generated by Django 3.1.1 on 2020-11-04 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0008_auto_20201029_0058'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessons',
            name='auditory',
            field=models.CharField(max_length=20, null=True, verbose_name='Аудитория'),
        ),
    ]