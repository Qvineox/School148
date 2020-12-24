import datetime

import pytz
from django.core.exceptions import ValidationError

from .models import LoanReceipts

from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'


class BookAddForm(forms.ModelForm):

    def clean(self):
        utc = pytz.UTC
        cleaned_data = super(BookAddForm, self).clean()
        recall_time = cleaned_data.get('recall_date')
        if recall_time:
            if utc.localize(datetime.datetime.today()) >= recall_time:
                msg = "Указанная вами дата находится в прошлом"
                self.add_error('recall_date', msg)
            elif utc.localize(datetime.datetime.today() + datetime.timedelta(days=367)) <= recall_time:
                msg = "Указанная вами дата превышает максимальный лимит"
                self.add_error('recall_date', msg)
        return cleaned_data

    class Meta:
        model = LoanReceipts
        fields = ['recall_date', 'book', 'borrower']

        widgets = {
            'recall_date': DateInput(),
            'book':  forms.HiddenInput(),
            'borrower': forms.HiddenInput()
        }


