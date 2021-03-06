# Generated by Django 3.1.1 on 2020-10-16 12:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0004_auto_20201016_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='apprentices',
            name='register_date',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Дата регистрации'),
        ),
        migrations.AddField(
            model_name='teachers',
            name='registered',
            field=models.BooleanField(default=False, verbose_name='Зарегистрирован'),
        ),
        migrations.AlterField(
            model_name='apprentices',
            name='email',
            field=models.TextField(max_length=30, verbose_name='Электронная почта'),
        ),
        migrations.AlterField(
            model_name='apprentices',
            name='phone',
            field=models.TextField(max_length=20, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='teachers',
            name='email',
            field=models.TextField(max_length=30, null=True, verbose_name='Электронная почта'),
        ),
        migrations.AlterField(
            model_name='teachers',
            name='phone',
            field=models.TextField(max_length=20, null=True, verbose_name='Телефон'),
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30, verbose_name='Имя')),
                ('second_name', models.CharField(max_length=30, verbose_name='Фамилия')),
                ('last_name', models.CharField(max_length=30, null=True, verbose_name='Отчество')),
                ('birth_date', models.DateField(verbose_name='Дата рождения')),
                ('phone', models.TextField(max_length=20, null=True, verbose_name='Телефон')),
                ('email', models.TextField(max_length=30, verbose_name='Электронная почта')),
                ('civ_id', models.CharField(max_length=30, verbose_name='Документ')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Аккаунт')),
            ],
        ),
    ]
