from django.conf import settings
from django.db import models


# Create your models here.

class Books(models.Model):
    ISBN_number = models.CharField(max_length=25, null=False, blank=False, primary_key=True, verbose_name='Номер ISBN')

    title = models.CharField(max_length=100, null=False, blank=False, unique=True, verbose_name='Название')
    author = models.CharField(max_length=100, null=False, blank=False, verbose_name='Автор')
    age_restriction = models.PositiveSmallIntegerField(null=True, blank=False, verbose_name='Ограничение по возрасту')

    # флаги и счетчики
    available = models.BooleanField(null=False, default=False, verbose_name='Наличие')
    stock = models.IntegerField(null=False, default=0, verbose_name='Осталось экземпляров')

    # отношения
    subject = models.ForeignKey('journal.Disciples', null=True, blank=False, on_delete=models.CASCADE,
                                verbose_name='Предмет')

    # def __str__(self):
    #     return self.title


class LoanReceipts(models.Model):
    book = models.ForeignKey('library.Books', null=False, blank=False, on_delete=models.CASCADE,
                             verbose_name='ISBN книги')

    borrow_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата заема')
    recall_date = models.DateTimeField(null=True, verbose_name='Дата возврата')

    # отношения
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False, on_delete=models.CASCADE,
                                 verbose_name='Аккаунт заемщика')