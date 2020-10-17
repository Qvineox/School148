from django import forms


class LoginForm(forms.Form):
    login = forms.CharField(label='login', max_length=150),
    password = forms.CharField(label='password', max_length=128)
