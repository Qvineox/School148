# Generated by Django 3.1.1 on 2020-10-16 20:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
        ('journal', '0003_auto_20201016_2339'),
    ]

    operations = [
        migrations.AddField(
            model_name='homework',
            name='deadline_lesson',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='schedule.lessons', verbose_name='Урок сдачи'),
        ),
        migrations.AddField(
            model_name='homework',
            name='placement_lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='schedule.lessons', verbose_name='Урок установки'),
        ),
    ]
