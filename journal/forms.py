from django import forms


class MarkPlacementForm(forms.Form):
    holder = forms.ChoiceField(label='holder', required=True)
    value = forms.ChoiceField(label='value', required=True)
    weight = forms.ChoiceField(label='weight', required=False)

    comment = forms.CharField(label='comment', required=False)
