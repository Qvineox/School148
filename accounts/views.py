from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from accounts.forms import *


def account_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user_login = form.data.get('login')
            user_password = form.data.get('password')

            print('{0}, {1}'.format(user_login, user_password))
            user = authenticate(request, username=user_login, password=user_password)

            if user is not None:
                login(request, user)
                print('success')
            else:
                print('failure')

        else:
            print('failure')

    return render(request, 'registration/login.html')


def account_preregister(request):
    if request.method == 'POST':
        form = PreRegisterForm(request.POST)

        if form.is_valid():
            # print(form.cleaned_data)

            request.session['new_user_data'] = form.cleaned_data
            return redirect('/accounts/registration')
        else:
            print('failure')

    return render(request, 'registration/preregister.html')


def account_register(request):
    user_data = request.session['new_user_data']
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            pass

    return render(request, 'registration/register.html', {'user_name': user_data['first_name'],
                                                          'user_last_name': user_data['last_name']})
