from django import forms

MARK_CHOICES = (
    (5, 'Отлично'),
    (4, 'Хорошо'),
    (3, 'Удовлетворительно'),
    (2, 'Неудовлетворительно'),
    (1, 'Плохо')
)

WEIGHT_CHOICES = (
    (4, 'Контрольная работа'),
    (3, 'Тест/Проверочная работа'),
    (2, 'Работа на уроке'),
    (1, 'Домашняя работа')
)


class MarkPlacementForm(forms.Form):
    holder = forms.IntegerField(label='holder', required=True)
    value = forms.ChoiceField(label='value', required=True, choices=MARK_CHOICES)
    weight = forms.ChoiceField(label='weight', required=False, choices=WEIGHT_CHOICES)

    comment = forms.CharField(label='comment', required=False)


class HomeworkPlacementForm(forms.Form):
    content = forms.CharField(label='content', required=True)
    file = forms.FileField(label='file', required=False)

    required = forms.BooleanField(label='requirement')
    deadline_date = forms.DateField(label='deadline_date')
