# Generated by Django 3.1.1 on 2020-11-20 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_auto_20201120_1356'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teachers',
            name='supervision_group',
        ),
        migrations.AddField(
            model_name='studygroups',
            name='supervisor',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='accounts.teachers', verbose_name='Куратор'),
        ),
        migrations.AlterField(
            model_name='apprentices',
            name='profile_picture',
            field=models.ImageField(null=True, upload_to='profile_images/', verbose_name='Картинка профиля'),
        ),
    ]
