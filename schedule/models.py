from django.db import models


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

    order = models.SmallIntegerField(choices=ORDER_CHOICES, null=True, blank=False, verbose_name='Порядковый номер')
    date = models.DateTimeField(null=False, blank=False, verbose_name='Дата урока')

    # флаги
    active = models.BooleanField(null=False, default=True, verbose_name='Активность')

    # отношения
    subject = models.ForeignKey('journal.Disciples', on_delete=models.CASCADE, null=True, verbose_name='Предмет')
    teacher = models.ForeignKey('accounts.Teachers', on_delete=models.CASCADE, null=True, verbose_name='Преподаватель')
    study_group = models.ForeignKey('accounts.StudyGroups', on_delete=models.CASCADE, null=True, verbose_name='Класс')
    homework = models.ForeignKey('journal.Homework', on_delete=models.CASCADE, null=True,
                                 verbose_name='Домашнее задание')
