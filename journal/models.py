import os

from django.conf import settings
from django.db import models


# таблица всех доступный предметов
class Disciples(models.Model):
    title = models.CharField(max_length=30, null=False, blank=False, verbose_name='Название')
    start_grade = models.PositiveSmallIntegerField(null=False, blank=False, verbose_name='Начальный класс')
    end_grade = models.PositiveSmallIntegerField(null=False, blank=False, verbose_name='Конечный класс')

    # цветовая схема предмета (для визуальной дифференциации), сопоставляется с одноименными стилями css
    scheme = models.CharField(max_length=20, null=False, blank=False, default='empty',
                              verbose_name='Цветовая схема')

    # флаги
    active = models.BooleanField(null=False, default=False, verbose_name='Активность')

    # отношения
    supervisor = models.ForeignKey('accounts.Managers', null=True, blank=False, on_delete=models.CASCADE,
                                   related_name='+', verbose_name='Руководитель')
    methodist = models.ForeignKey('accounts.Managers', null=True, blank=False, on_delete=models.CASCADE,
                                  related_name='+', verbose_name='Методист')

    def __str__(self):
        return self.title


# все поставленные оценки
class Marks(models.Model):
    EXCELLENT = 5
    GOOD = 4
    NORMAL = 3
    BAD = 2
    WORST = 1
    ABSENT = 0

    MARK_CHOICES = (
        (EXCELLENT, 'Отлично'),
        (GOOD, 'Хорошо'),
        (NORMAL, 'Удовлетворительно'),
        (BAD, 'Неудовлетворительно'),
        (WORST, 'Плохо'),
        (ABSENT, 'Отсутсвует'),
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

    weight = models.SmallIntegerField(choices=WEIGHT_CHOICES, null=True, default=1, verbose_name='Вес')
    comment = models.TextField(null=True, blank=False, verbose_name='Комментарий')
    rating_date = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата установки')
    modify_date = models.DateTimeField(auto_now=True, null=True, verbose_name='Дата изменения')

    # отношения
    holder = models.ForeignKey('accounts.Apprentices', null=False, on_delete=models.CASCADE, verbose_name='Получатель')
    appraiser = models.ForeignKey('accounts.Teachers', null=False, on_delete=models.CASCADE,
                                  verbose_name='Постановитель')
    lesson = models.ForeignKey('Lessons', null=True, on_delete=models.CASCADE, verbose_name='Урок')


def homework_path():
    return os.path.join(settings.LOCAL_FILE_DIR, 'homeworks')


# все домашние задания
class Homeworks(models.Model):
    text = models.TextField(null=False, blank=False, verbose_name='Текст домашнего задания')
    file = models.FilePathField(path=homework_path, null=True, match=".*\.zip$|.*\.pdf$|.*\.png$|.*\.jpeg$",
                                verbose_name='Файл домашнего задания')

    # флаги
    required = models.BooleanField(default=True, null=False, verbose_name='Обязательность выполнения')

    # отношения
    author = models.ForeignKey('accounts.Teachers', null=True, on_delete=models.CASCADE, verbose_name='Автор')
    placement_lesson = models.ForeignKey('Lessons', null=False, on_delete=models.CASCADE,
                                         related_name='+', verbose_name='Урок установки')
    deadline_lesson = models.ForeignKey('Lessons', null=True, on_delete=models.CASCADE,
                                        related_name='+', verbose_name='Урок сдачи')
    deadline_time = models.DateTimeField(null=False, blank=False, verbose_name='Срок сдачи')

    # вспомогательные поля
    target_group = models.ForeignKey('accounts.StudyGroups', null=True, blank=False, on_delete=models.CASCADE,
                                     verbose_name='Учебная группа')

    def __str__(self):
        return self.text


class Specialization(models.Model):
    title = models.CharField(max_length=30, null=False, blank=False, verbose_name='Название')

    # отношения
    main_disciple = models.ForeignKey('Disciples', null=True, on_delete=models.CASCADE, verbose_name='Дисциплина')


class Lessons(models.Model):
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4
    FIFTH = 5
    SIXTH = 6
    SEVENTH = 7
    EIGHTH = 8
    NINTH = 9
    TENTH = 10

    ORDER_CHOICES = (
        (FIRST, 'Первый'),
        (SECOND, 'Второй'),
        (THIRD, 'Третий'),
        (FOURTH, 'Четвертый'),
        (FIFTH, 'Пятый'),
        (SIXTH, 'Шестой'),
        (SEVENTH, 'Седьмой'),
        (EIGHTH, 'Восьмой'),
        (NINTH, 'Девятый'),
        (TENTH, 'Десятый')
    )

    order = models.SmallIntegerField(choices=ORDER_CHOICES, null=False, blank=False, verbose_name='Порядковый номер')
    date = models.DateField(null=False, blank=False, verbose_name='Дата урока')
    auditory = models.CharField(null=True, blank=False, max_length=20, verbose_name='Аудитория')

    # флаги
    active = models.BooleanField(null=False, default=True, verbose_name='Активность')

    # отношения
    subject = models.ForeignKey('Disciples', related_name='subject', on_delete=models.CASCADE, null=False,
                                verbose_name='Предмет')
    teacher = models.ForeignKey('accounts.Teachers', related_name='teacher', on_delete=models.CASCADE, null=False,
                                verbose_name='Преподаватель')
    study_group = models.ForeignKey('accounts.StudyGroups', on_delete=models.CASCADE, null=False, verbose_name='Класс')
    homework = models.ForeignKey('Homeworks', related_name='homework', on_delete=models.CASCADE, null=True,
                                 verbose_name='Домашнее задание')

    class Meta:
        ordering = ['date', 'order']

    def __str__(self):
        return self.subject.title
