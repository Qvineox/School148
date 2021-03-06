# Generated by Django 3.1.1 on 2020-10-17 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20201017_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='managers',
            name='position',
            field=models.CharField(choices=[('PR', 'Principal'), ('DEW', 'Deputy of Educational Work'), ('DS', 'Deputy of Security'), ('DEA', 'Deputy of Administration and Economics'), ('SM', 'Subject Methodist'), ('GM', 'General Methodist'), ('ADM', 'Accounting Department Member'), ('ADH', 'Head of Accounting Department'), ('EDM', 'Education Department Member'), ('EDH', 'Head of Education Department'), ('HPAC', 'Head of Parental Advice Council'), ('GBM', 'Governing Council Member'), ('GBH', 'Head of Governing Council'), ('LUA', 'Labor Union Agent'), ('CL', 'Chief Librarian'), ('THW', 'Temporary Hired Worker')], default='THW', max_length=30),
        ),
    ]
