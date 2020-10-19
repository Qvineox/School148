from django import forms


class LoginForm(forms.Form):
    login = forms.CharField(label='login', max_length=150, required=True)
    password = forms.CharField(label='password', max_length=128, widget=forms.PasswordInput(), required=True)


class PreRegisterForm(forms.Form):
    first_name = forms.CharField(label='first_name', max_length=30, required=True)
    second_name = forms.CharField(label='second_name', max_length=30, required=True)
    last_name = forms.CharField(label='last_name', max_length=30, required=False)

    phone_number = forms.CharField(label='phone_number', max_length=20, required=False)
    email = forms.EmailField(label='email', required=False)


class RegisterForm(forms.Form):
    login = forms.CharField(label='login', max_length=150, required=True)
    password = forms.CharField(label='password', max_length=128, widget=forms.PasswordInput(), required=True)

