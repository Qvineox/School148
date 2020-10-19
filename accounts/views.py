from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from accounts.forms import *
from accounts.services import *


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
            check = check_account_availability(form.cleaned_data['role'],
                                               form.cleaned_data['first_name'],
                                               form.cleaned_data['second_name'])

            if type(check) == bool:
                if check:
                    request.session['new_user_data'] = form.cleaned_data
                    return redirect('/accounts/registration')
                else:
                    print('failure: 1+')
            else:
                message = check
                print(message)

        else:
            print('failure')

    return render(request, 'registration/preregister.html')


def account_register(request):
    user_data = request.session['new_user_data']
    print(user_data)
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['login'],
                                            password=form.cleaned_data['password'],
                                            first_name=user_data['first_name'],
                                            last_name=user_data['last_name'],
                                            email=user_data['email'],
                                            )

            if int(user_data['role']) > 2:
                user.is_staff = True
                if int(user_data['role']) > 4:
                    user.is_superuser = True

            user.save()
            return redirect('/accounts/login')

    return render(request, 'registration/register.html', {'user_name': user_data['first_name'],
                                                          'user_last_name': user_data['last_name']})
