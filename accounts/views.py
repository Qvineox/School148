from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

from accounts.forms import *
from accounts.services import *

logger = logging.getLogger('auth')


def account_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user_login = form.data.get('login')
            user_password = form.data.get('password')

            user = authenticate(request, username=user_login, password=user_password)

            if user is not None:
                login(request, user)
                logger.info('User logged: {0}'.format(user_login))
                print('success')
            else:
                if User.objects.filter(username=user_login).count() > 0:
                    reason = 'Incorrect password.'
                    messages.warning(request, 'Неправильный пароль. Попробуйте еще раз.')
                else:
                    reason = 'Account not found.'
                    messages.error(request, 'Записи с такими данными не существует. Обратитесь к своему куратору.')

                logger.warning('User {0} login failed: {1}'.format(user_login, reason))

        else:
            logger.warning('Invalid form received from user.')

    return render(request, 'registration/login.html')


def account_preregister(request):
    if request.method == 'POST':
        form = PreRegisterForm(request.POST)

        if form.is_valid():
            check = check_account_availability(form.cleaned_data['role'],
                                               form.cleaned_data['first_name'],
                                               form.cleaned_data['second_name'])
            if type(check) == int:
                # check содержит id записи в школьной структуре
                request.session['new_user_data'] = form.cleaned_data
                request.session['new_user_account_id'] = check
                logger.info(
                    'User validated to register: role={0}, school_id={1}'.format(form.cleaned_data['role'], check))
                return redirect('/accounts/registration')
            else:
                message = check
                logger.warning('User register failed: {0}, reason: {1}'.format(form.cleaned_data, message))
                messages.warning(request, message)

        else:
            logger.warning('Invalid form received from user.')
            messages.error(request, 'Форма заполнена некорректно. Повторите заполнение.')

    return render(request, 'registration/preregister.html')


def account_register(request):
    user_data = request.session['new_user_data']

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            # проверяем, что нет пользователей с таким username
            if not User.objects.filter(username=form.cleaned_data['login']).count() > 0:
                # создаем пользователя и соединяем его с записью в школьной структуре
                user = User.objects.create_user(username=form.cleaned_data['login'],
                                                password=form.cleaned_data['password'],
                                                first_name=user_data['first_name'],
                                                last_name=user_data['last_name'],
                                                email=user_data['email'],
                                                )

                user_group = Group.objects.get(id=user_data['role'])
                user_group.user_set.add(user)

                if int(user_data['role']) > 2:
                    user.is_staff = True
                    if int(user_data['role']) > 4:
                        user.is_superuser = True

                user_group.save()
                user.save()
                connect_account_to_record(user_data['role'], user.id, request.session['new_user_account_id'])

                logger.info('New user registered: {0}'.format(user))
                return redirect('/accounts/login')
            else:
                logger.warning('Account with given username already exists: {0}'.format(form.cleaned_data['login']))
                messages.warning(request, 'Аккаунт с таким именем пользователя уже существует. Попробуйте другое.')
        else:
            logger.warning('Invalid form received from user.')
            messages.error(request, 'Форма заполнена некорректно. Повторите заполнение.')

    return render(request, 'registration/register.html', {'user_name': user_data['first_name'],
                                                          'user_last_name': user_data['last_name']})


def profile(request, user_id):
    if user_id is not None:
        user_data = get_profile_data(user_id)
    else:
        user_data = get_profile_data(request.user.id)

    return render(request, 'profiles/apprentice_page.html', navbar_data(request))


def navbar_data(request):
    data = get_profile_data(request.user.id)

    data = {
        'first_name': data.first_name,
        'second_name': data.second_name,
        'last_name': data.last_name,
        'id': data.id
    }

    return data
