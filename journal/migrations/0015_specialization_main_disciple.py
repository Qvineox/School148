# Generated by Django 3.1.1 on 2020-11-20 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0014_auto_20201119_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='specialization',
            name='main_disciple',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='journal.disciples', verbose_name='Дисциплина'),
        ),
    ]
