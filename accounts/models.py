from django.conf import settings
from django.db import models


# данные школьников
class Apprentices(models.Model):
    # личная информация
    first_name = models.CharField(max_length=30, null=False, blank=False, verbose_name='Имя')
    second_name = models.CharField(max_length=30, null=False, blank=False, verbose_name='Фамилия')
    last_name = models.CharField(max_length=30, null=True, blank=False, verbose_name='Отчество')
    birth_date = models.DateField(null=False, blank=False, verbose_name='Дата рождения')
    phone = models.TextField(null=True, blank=False, max_length=20, verbose_name='Телефон')
    email = models.TextField(null=True, blank=False, max_length=30, verbose_name='Электронная почта')
    civ_id = models.CharField(null=False, blank=False, max_length=30, verbose_name='Документ')

    # флаги
    active = models.BooleanField(null=False, default=False, verbose_name='Активность')

    # отношения
    # study_group = models.ForeignKey(Study_groups, on_delete=models.CASCADE)

    # father = models.ForeignKey(Parents, on_delete=models.CASCADE)
    # mother = models.ForeignKey(Parents, on_delete=models.CASCADE)

    # учетные данные
    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Аккаунт')


# данные учителей
class Teachers(models.Model):
    # личная информация
    first_name = models.CharField(max_length=30, null=False, blank=False, verbose_name='Имя')
    second_name = models.CharField(max_length=30, null=False, blank=False, verbose_name='Фамилия')
    last_name = models.CharField(max_length=30, null=True, blank=False, verbose_name='Отчество')
    birth_date = models.DateField(null=False, blank=False, verbose_name='Дата рождения')
    phone = models.TextField(null=False, blank=False, max_length=20, verbose_name='Телефон')
    email = models.TextField(null=False, blank=False, max_length=30, verbose_name='Электронная почта')
    civ_id = models.CharField(null=False, blank=False, max_length=30, verbose_name='Документ')

    # флаги
    active = models.BooleanField(null=False, default=False, verbose_name='Активность')

    # отношения
    # supervision_group = models.ForeignKey(Study_groups, on_delete=models.CASCADE, verbose_name='Кураторство')
    # disciple = models.ForeignKey(Disciples, on_delete=models.CASCADE, verbose_name='Специализация')

    # учетные данные
    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Аккаунт')


# учебные группы
class StudyGroups(models.Model):
    grade = models.PositiveSmallIntegerField(null=False, blank=False, verbose_name='Номер')
    symbol = models.CharField(max_length=1, null=False, blank=False, verbose_name='Буква')

    # отношения
    # specialisation = models.ForeignKey(Disciples, on_delete=models.CASCADE, verbose_name='Специализация')
    supervisor = models.ForeignKey(Teachers, on_delete=models.CASCADE, verbose_name='Куратор')
