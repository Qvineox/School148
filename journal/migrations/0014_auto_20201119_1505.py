# Generated by Django 3.1.1 on 2020-11-19 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_auto_20201018_1117'),
        ('journal', '0013_auto_20201119_1504'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Homework',
            new_name='Homeworks',
        ),
        migrations.RenameModel(
            old_name='Mark',
            new_name='Marks',
        ),
    ]
