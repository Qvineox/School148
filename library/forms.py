from .models import LoanReceipts

from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'


class BookAddForm(forms.ModelForm):
    class Meta:
        model = LoanReceipts
        fields = ['recall_date', 'book', 'borrower']
        widgets = {
            'recall_date': DateInput(),
            'book':  forms.HiddenInput(),
            'borrower': forms.HiddenInput()
        }
