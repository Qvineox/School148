from django.contrib.auth import views
from django.contrib.auth import authenticate, login
from django.shortcuts import render

from accounts.forms import LoginForm


def site_login(request):
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
