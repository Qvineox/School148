from django.conf import settings
from django.db import models


class StudyGroups(models.Model):
    grade = models.PositiveSmallIntegerField(null=False, blank=False, verbose_name='Номер')
    symbol = models.CharField(max_length=1, null=False, blank=False, verbose_name='Буква')

    # отношения
    specialisation = models.ForeignKey('journal.Specialization', null=True, on_delete=models.CASCADE,
                                       verbose_name='Специализация')


MALE = 'M'
FEMALE = 'Fe'
OTHER = 'Etc'


class CreativeGroups(models.Model):
    title = models.CharField(max_length=20, null=False, blank=False, verbose_name='Название')
    creation_date = models.DateTimeField(auto_now_add=True, null=False)
    requirements = models.TextField(null=True, blank=False)


class Parents(models.Model):
    first_name = models.CharField(max_length=30, null=False, blank=False, verbose_name='Имя')
    second_name = models.CharField(max_length=30, null=False, blank=False, verbose_name='Фамилия')
    last_name = models.CharField(max_length=30, null=True, blank=False, verbose_name='Отчество')
    gender = models.CharField(max_length=5, null=False, blank=False,
                              choices=[('M', 'Male'), ('Fe', 'Female'), ('Etc', 'Other')], default=OTHER)
    phone = models.TextField(null=True, blank=False, max_length=20, verbose_name='Телефон')
    email = models.TextField(null=False, blank=False, max_length=30, verbose_name='Электронная почта')

    # учетные данные
    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Аккаунт')
    registered = models.BooleanField(null=False, default=False, verbose_name='Зарегистрирован')


# данные школьников
class Apprentices(models.Model):
    # личная информация
    first_name = models.CharField(max_length=30, null=False, blank=False, verbose_name='Имя')
    second_name = models.CharField(max_length=30, null=False, blank=False, verbose_name='Фамилия')
    last_name = models.CharField(max_length=30, null=True, blank=False, verbose_name='Отчество')
    gender = models.CharField(max_length=5, null=False, blank=False,
                              choices=[('M', 'Male'), ('Fe', 'Female'), ('Etc', 'Other')], default=OTHER)
    birth_date = models.DateField(null=False, blank=False, verbose_name='Дата рождения')
    phone = models.TextField(null=True, blank=False, max_length=20, verbose_name='Телефон')
    email = models.TextField(null=True, blank=False, max_length=30, verbose_name='Электронная почта')
    civ_id = models.CharField(null=False, blank=False, max_length=30, verbose_name='Документ')

    profile_picture = models.FilePathField(null=True, match=".*\.png$|.*\.jpeg$",
                                           verbose_name='Картинка профиля')

    # флаги
    active = models.BooleanField(null=False, default=False, verbose_name='Активность')

    # отношения
    study_group = models.ForeignKey(StudyGroups, null=True, on_delete=models.CASCADE, verbose_name='Учебная группа')

    father = models.ForeignKey(Parents, null=True, on_delete=models.CASCADE, verbose_name='Отец', related_name='+')
    mother = models.ForeignKey(Parents, null=True, on_delete=models.CASCADE, verbose_name='Мать', related_name='+')

    creative_groups = models.ManyToManyField('accounts.CreativeGroups')

    # учетные данные
    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Аккаунт')
    register_date = models.DateField(null=True, auto_now_add=True, verbose_name='Дата регистрации')


# данные учителей
class Teachers(models.Model):
    # личная информация
    first_name = models.CharField(max_length=30, null=False, blank=False, verbose_name='Имя')
    second_name = models.CharField(max_length=30, null=False, blank=False, verbose_name='Фамилия')
    last_name = models.CharField(max_length=30, null=True, blank=False, verbose_name='Отчество')
    gender = models.CharField(max_length=5, null=False, blank=False,
                              choices=[('M', 'Male'), ('Fe', 'Female'), ('Etc', 'Other')], default=OTHER)
    birth_date = models.DateField(null=False, blank=False, verbose_name='Дата рождения')
    phone = models.TextField(null=False, blank=False, max_length=20, verbose_name='Телефон')
    email = models.TextField(null=False, blank=False, max_length=30, verbose_name='Электронная почта')
    civ_id = models.CharField(null=False, blank=False, max_length=30, verbose_name='Документ')

    # флаги
    active = models.BooleanField(null=False, default=False, verbose_name='Активность')

    # отношения
    supervision_group = models.ForeignKey(StudyGroups, null=True, on_delete=models.CASCADE, verbose_name='Кураторство')
    disciple = models.ForeignKey('journal.Disciples', null=True, on_delete=models.CASCADE, verbose_name='Специализация')

    # учетные данные
    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Аккаунт')
    registered = models.BooleanField(null=False, default=False, verbose_name='Зарегистрирован')


# данные персонала
class Staff(models.Model):
    first_name = models.CharField(max_length=30, null=False, blank=False, verbose_name='Имя')
    second_name = models.CharField(max_length=30, null=False, blank=False, verbose_name='Фамилия')
    last_name = models.CharField(max_length=30, null=True, blank=False, verbose_name='Отчество')
    gender = models.CharField(max_length=5, null=False, blank=False,
                              choices=[('M', 'Male'), ('Fe', 'Female'), ('Etc', 'Other')], default=OTHER)
    birth_date = models.DateField(null=False, blank=False, verbose_name='Дата рождения')
    phone = models.TextField(null=True, blank=False, max_length=20, verbose_name='Телефон')
    email = models.TextField(null=False, blank=False, max_length=30, verbose_name='Электронная почта')
    civ_id = models.CharField(null=False, blank=False, max_length=30, verbose_name='Документ')

    # учетные данные
    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Аккаунт')
    registered = models.BooleanField(null=False, default=False, verbose_name='Зарегистрирован')


# управляющий коллектив
class Managers(models.Model):
    first_name = models.CharField(max_length=30, null=False, blank=False, verbose_name='Имя')
    second_name = models.CharField(max_length=30, null=False, blank=False, verbose_name='Фамилия')
    last_name = models.CharField(max_length=30, null=True, blank=False, verbose_name='Отчество')
    gender = models.CharField(max_length=5, null=False, blank=False,
                              choices=[('M', 'Male'), ('Fe', 'Female'), ('Etc', 'Other')], default=OTHER)
    birth_date = models.DateField(null=False, blank=False, verbose_name='Дата рождения')
    phone = models.TextField(null=True, blank=False, max_length=20, verbose_name='Телефон')
    email = models.TextField(null=False, blank=False, max_length=30, verbose_name='Электронная почта')
    civ_id = models.CharField(null=False, blank=False, max_length=30, verbose_name='Документ')

    # организационная информация
    position = models.CharField(max_length=30, null=False, blank=False,
                                choices=[
                                    # директор
                                    ('PR', 'Principal'),
                                    # заместитель по воспитательной работе
                                    ('DEW', 'Deputy of Educational Work'),
                                    # заместитель по безопасности
                                    ('DS', 'Deputy of Security'),
                                    # заместитель по административно-хозяйственной части
                                    ('DEA', 'Deputy of Administration and Economics'),
                                    # предметный методист
                                    ('SM', 'Subject Methodist'),
                                    # методист общего образовательного процесса
                                    ('GM', 'General Methodist'),
                                    # работник бухгалтерии
                                    ('ADM', 'Accounting Department Member'),
                                    # глава бухгалтерии
                                    ('ADH', 'Head of Accounting Department'),
                                    # член педагогического совета
                                    ('EDM', 'Education Department Member'),
                                    # глава педагогического совета
                                    ('EDH', 'Head of Education Department'),
                                    # глава родительского комитета
                                    ('HPAC', 'Head of Parental Advice Council'),
                                    # глава управляющего совета
                                    ('GBM', 'Governing Council Member'),
                                    # глава управляющего совета
                                    ('GBH', 'Head of Governing Council'),
                                    # агент профсоюза
                                    ('LUA', 'Labor Union Agent'),
                                    # главный библиотекарь
                                    ('CL', 'Chief Librarian'),
                                    # наемный сотрудник
                                    ('THW', 'Temporary Hired Worker')
                                ], default='THW')

    # учетные данные
    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=False,
                                verbose_name='Аккаунт')
    registered = models.BooleanField(null=False, default=False, verbose_name='Зарегистрирован')
