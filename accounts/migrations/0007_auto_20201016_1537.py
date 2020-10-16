# Generated by Django 3.1.1 on 2020-10-16 12:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0006_auto_20201016_1519'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studygroups',
            name='supervisor',
        ),
        migrations.AddField(
            model_name='apprentices',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('Fe', 'Female'), ('Etc', 'Other')], default='Etc', max_length=5),
        ),
        migrations.AddField(
            model_name='apprentices',
            name='study_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.studygroups'),
        ),
        migrations.AddField(
            model_name='staff',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('Fe', 'Female'), ('Etc', 'Other')], default='Etc', max_length=5),
        ),
        migrations.AddField(
            model_name='staff',
            name='registered',
            field=models.BooleanField(default=False, verbose_name='Зарегистрирован'),
        ),
        migrations.AddField(
            model_name='teachers',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('Fe', 'Female'), ('Etc', 'Other')], default='Etc', max_length=5),
        ),
        migrations.AddField(
            model_name='teachers',
            name='supervision_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.studygroups', verbose_name='Кураторство'),
        ),
        migrations.CreateModel(
            name='Parents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30, verbose_name='Имя')),
                ('second_name', models.CharField(max_length=30, verbose_name='Фамилия')),
                ('last_name', models.CharField(max_length=30, null=True, verbose_name='Отчество')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('Fe', 'Female'), ('Etc', 'Other')], default='Etc', max_length=5)),
                ('phone', models.TextField(max_length=20, null=True, verbose_name='Телефон')),
                ('email', models.TextField(max_length=30, verbose_name='Электронная почта')),
                ('registered', models.BooleanField(default=False, verbose_name='Зарегистрирован')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Аккаунт')),
            ],
        ),
        migrations.AddField(
            model_name='apprentices',
            name='father',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='accounts.parents', verbose_name='Отец'),
        ),
        migrations.AddField(
            model_name='apprentices',
            name='mother',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='accounts.parents', verbose_name='Мать'),
        ),
    ]
