from django import forms


class LoginForm(forms.Form):
    login = forms.CharField(label='login', max_length=150, required=True)
    password = forms.CharField(label='password', max_length=128, widget=forms.PasswordInput(), required=True)


class PreRegisterForm(forms.Form):
    first_name = forms.CharField(label='first_name', max_length=30, required=True)
    second_name = forms.CharField(label='second_name', max_length=30, required=True)
    last_name = forms.CharField(label='last_name', max_length=30, required=False)

    CHOICES = [('1', 'Apprentice'),
               ('2', 'Parent'),
               ('3', 'Staff'),
               ('4', 'Teacher'),
               ('5', 'Managers'),
               ('6', 'Administration')]

    role = forms.ChoiceField(label='role', widget=forms.Select, choices=CHOICES, required=True)

    phone_number = forms.CharField(label='phone_number', max_length=20, required=False)
    email = forms.EmailField(label='email', required=False)


class RegisterForm(forms.Form):
    login = forms.CharField(label='login', max_length=150, required=True)
    password = forms.CharField(label='password', max_length=128, widget=forms.PasswordInput(), required=True)


class ProfileEditForm(forms.Form):
    email = forms.CharField(label='email', max_length=30, required=True)
    phone = forms.CharField(label='phone', max_length=30, required=True)
    status = forms.CharField(label='status', max_length=30, required=False)

    profile_image = forms.ImageField(label='profile_image', allow_empty_file=True, required=False)
