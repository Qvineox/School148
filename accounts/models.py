from django.conf import settings
from django.db import models


class StudyGroups(models.Model):
    grade = models.PositiveSmallIntegerField(null=False, blank=False, verbose_name='Номер')
    symbol = models.CharField(max_length=1, null=False, blank=False, verbose_name='Буква')

    # отношения
    specialisation = models.ForeignKey('journal.Specialization', null=True, on_delete=models.CASCADE,
                                       verbose_name='Специализация')
    supervisor = models.ForeignKey('Teachers', null=True, on_delete=models.CASCADE, verbose_name='Куратор')
    methodist = models.ForeignKey('Managers', null=True, on_delete=models.CASCADE, verbose_name='Методист')
    headman = models.ForeignKey('Apprentices', null=True, on_delete=models.CASCADE, verbose_name='Староста')


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
    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, unique=True,
                                   verbose_name='Аккаунт')
    active = models.BooleanField(null=False, default=False, verbose_name='Зарегистрирован')

    # медиа
    profile_picture = models.ImageField(null=True, upload_to='profile_images/',
                                        verbose_name='Картинка профиля')


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

    # медиа
    profile_picture = models.ImageField(null=True, upload_to='profile_images/', default='profile_images/default.png',
                                        verbose_name='Картинка профиля')

    # флаги
    active = models.BooleanField(null=False, default=False, verbose_name='Активность')

    # отношения
    study_group = models.ForeignKey(StudyGroups, null=True, on_delete=models.CASCADE, verbose_name='Учебная группа')

    father = models.ForeignKey(Parents, null=True, on_delete=models.CASCADE, verbose_name='Отец', related_name='+')
    mother = models.ForeignKey(Parents, null=True, on_delete=models.CASCADE, verbose_name='Мать', related_name='+')

    creative_groups = models.ManyToManyField('accounts.CreativeGroups')

    # учетные данные
    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, unique=True,
                                   verbose_name='Аккаунт')
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
    disciple = models.ForeignKey('journal.Disciples', null=True, on_delete=models.CASCADE, verbose_name='Специализация')

    # учетные данные
    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, unique=True,
                                   verbose_name='Аккаунт')

    # медиа
    profile_picture = models.ImageField(null=True, upload_to='profile_images/', default='profile_images/default.png',
                                        verbose_name='Картинка профиля')


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
    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                   verbose_name='Аккаунт')
    active = models.BooleanField(null=False, default=False, verbose_name='Зарегистрирован')

    # медиа
    profile_picture = models.ImageField(null=True, upload_to='profile_images/', default='profile_images/default.png',
                                        verbose_name='Картинка профиля')


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
                                    ('PR', 'Директор'),
                                    # заместитель по воспитательной работе
                                    ('DEW', 'Заместитель по Воспитательной Работе'),
                                    # заместитель по безопасности
                                    ('DS', 'Заместитель по Безопасности'),
                                    # заместитель по административно-хозяйственной части
                                    ('DEA', 'Заместитель по Административно-хозяйственной Части'),
                                    # предметный методист
                                    ('SM', 'Предметный Методист'),
                                    # методист общего образовательного процесса
                                    ('GM', 'Методист Общего Образовательного Процесса'),
                                    # работник бухгалтерии
                                    ('ADM', 'Работник Бухгалтерии'),
                                    # глава бухгалтерии
                                    ('ADH', 'Глава Бухгалтерии'),
                                    # член педагогического совета
                                    ('EDM', 'Член Педагогического Совета'),
                                    # глава педагогического совета
                                    ('EDH', 'Глава Педагогического Совета'),
                                    # глава родительского комитета
                                    ('HPAC', 'Глава Родительского Комитета'),
                                    # глава управляющего совета
                                    ('GBM', 'Глава Управляющего Совета'),
                                    # глава управляющего совета
                                    ('GBH', 'Глава Управляющего Совета'),
                                    # агент профсоюза
                                    ('LUA', 'Агент Профсоюза'),
                                    # главный библиотекарь
                                    ('CL', 'Главный Библиотекарь'),
                                    # наемный сотрудник
                                    ('THW', 'Наемный Сотрудник')
                                ], default='THW')

    # учетные данные
    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, unique=False,
                                   verbose_name='Аккаунт')
    active = models.BooleanField(null=False, default=False, verbose_name='Зарегистрирован')

    # медиа
    profile_picture = models.ImageField(null=True, upload_to='profile_images/', default='profile_images/default.png',
                                        verbose_name='Картинка профиля')

    # методы
    def __str__(self):
        return self.get_position_display()
