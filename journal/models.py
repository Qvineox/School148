import os

from django.conf import settings
from django.db import models


# таблица всех доступный предметов
class Disciples(models.Model):
    title = models.CharField(max_length=30, null=False, blank=False, verbose_name='Название')
    start_grade = models.PositiveSmallIntegerField(null=False, blank=False, verbose_name='Начальный класс')
    end_grade = models.PositiveSmallIntegerField(null=False, blank=False, verbose_name='Конечный класс')

    # флаги
    active = models.BooleanField(null=False, default=False, verbose_name='Активность')

    # отношения
    supervisor = models.ForeignKey('accounts.Managers', null=True, blank=False, on_delete=models.CASCADE,
                                   related_name='+', verbose_name='Руководитель')
    methodist = models.ForeignKey('accounts.Managers', null=True, blank=False, on_delete=models.CASCADE,
                                  related_name='+', verbose_name='Методист')


# все поставленные оценки
class Mark(models.Model):
    EXCELLENT = 5
    GOOD = 4
    NORMAL = 3
    BAD = 2
    WORST = 1

    MARK_CHOICES = (
        (EXCELLENT, 'Отлично'),
        (GOOD, 'Хорошо'),
        (NORMAL, 'Удовлетворительно'),
        (BAD, 'Неудовлетворительно'),
        (WORST, 'Плохо'),
    )

    value = models.SmallIntegerField(choices=MARK_CHOICES, null=False, verbose_name='Значение')

    EXAM = 4
    TEST = 3
    CLASSWORK = 2
    HOMEWORK = 1

    WEIGHT_CHOICES = (
        (EXAM, 'Контрольная работа'),
        (TEST, 'Тест/Проверочная работа'),
        (CLASSWORK, 'Работа на уроке'),
        (HOMEWORK, 'Домашняя работа')
    )

    weight = models.SmallIntegerField(choices=WEIGHT_CHOICES, null=False, default=2, verbose_name='Вес')
    comment = models.TextField(null=True, blank=False, verbose_name='Комментарий')
    rating_date = models.DateTimeField(auto_now_add=True, null=False, verbose_name='Дата установки')
    modify_date = models.DateTimeField(auto_now=True, null=False, verbose_name='Дата изменения')

    # отношения
    holder = models.ForeignKey('accounts.Apprentices', null=False, on_delete=models.CASCADE, verbose_name='Получатель')
    appraiser = models.ForeignKey('accounts.Teachers', null=False, on_delete=models.CASCADE,
                                  verbose_name='Постановитель')
    lesson = models.ForeignKey('schedule.Lessons', null=True, on_delete=models.CASCADE, verbose_name='Урок')


def homework_path():
    return os.path.join(settings.LOCAL_FILE_DIR, 'homeworks')


# все домашние задания
class Homework(models.Model):
    text = models.TextField(null=False, blank=False, verbose_name='Текст домашнего задания')
    file = models.FilePathField(path=homework_path, null=True, match=".*\.zip$|.*\.pdf$|.*\.png$|.*\.jpeg$",
                                verbose_name='Файл домашнего задания')

    # флаги
    required = models.BooleanField(default=True, null=False, verbose_name='Обязательность выполнения')

    # отношения
    author = models.ForeignKey('accounts.Teachers', null=True, on_delete=models.CASCADE, verbose_name='Автор')
    placement_lesson = models.ForeignKey('schedule.Lessons', null=False, on_delete=models.CASCADE,
                                         related_name='+', verbose_name='Урок установки')
    deadline_lesson = models.ForeignKey('schedule.Lessons', null=True, on_delete=models.CASCADE,
                                        related_name='+', verbose_name='Урок сдачи')
    deadline_time = models.DateTimeField(null=False, blank=False, verbose_name='Срок сдачи')


class Specialization(models.Model):
    title = models.CharField(max_length=30, null=False, blank=False, verbose_name='Название')
