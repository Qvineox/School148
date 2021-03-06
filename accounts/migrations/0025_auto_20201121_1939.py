# Generated by Django 3.1.1 on 2020-11-21 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_auto_20201121_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apprentices',
            name='profile_picture',
            field=models.ImageField(default='profile_images/default.png', null=True, upload_to='profile_images/', verbose_name='Картинка профиля'),
        ),
        migrations.AlterField(
            model_name='managers',
            name='profile_picture',
            field=models.ImageField(default='profile_images/default.png', null=True, upload_to='profile_images/', verbose_name='Картинка профиля'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='profile_picture',
            field=models.ImageField(default='profile_images/default.png', null=True, upload_to='profile_images/', verbose_name='Картинка профиля'),
        ),
        migrations.AlterField(
            model_name='teachers',
            name='profile_picture',
            field=models.ImageField(default='profile_images/default.png', null=True, upload_to='profile_images/', verbose_name='Картинка профиля'),
        ),
    ]
