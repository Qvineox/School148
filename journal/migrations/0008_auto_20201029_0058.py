# Generated by Django 3.1.1 on 2020-10-28 21:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_auto_20201018_1117'),
        ('journal', '0007_auto_20201029_0055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessons',
            name='order',
            field=models.SmallIntegerField(choices=[(1, 'Первый'), (2, 'Второй'), (3, 'Третий'), (4, 'Четвертый'), (5, 'Пятый'), (6, 'Шестой'), (7, 'Седьмой'), (8, 'Восьмой'), (9, 'Девятый'), (10, 'Десятый')], default=123, verbose_name='Порядковый номер'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lessons',
            name='study_group',
            field=models.ForeignKey(default=123, on_delete=django.db.models.deletion.CASCADE, to='accounts.studygroups', verbose_name='Класс'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lessons',
            name='subject',
            field=models.ForeignKey(default=123, on_delete=django.db.models.deletion.CASCADE, to='journal.disciples', verbose_name='Предмет'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lessons',
            name='teacher',
            field=models.ForeignKey(default=123, on_delete=django.db.models.deletion.CASCADE, to='accounts.teachers', verbose_name='Преподаватель'),
            preserve_default=False,
        ),
    ]