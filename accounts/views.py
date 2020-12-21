from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect

from accounts.forms import *
from accounts.services import *
from home.views import navbar_data, toolbox_data
from statistic.services import get_teacher_average_score, get_apprentice_average_score, \
    get_apprentice_attendance_score, get_group_statistics, get_all_teacher_lessons

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
                if get_user_prior_group_number(user.id) > 4:
                    return redirect('settings')
                else:
                    return redirect('home')
                logger.info('User logged: {0}'.format(user_login))
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


def account_logout(request):
    logout(request)
    return redirect('login')


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


@login_required(login_url='/accounts/login/')
def user_profile(request):
    user_id = request.user.id
    user_data = get_profile_data(user_id)
    privilege_level = get_user_prior_group_number(user_id)
    tools = [('Редактировать', '../{0}/edit'.format(user_id)), ('Выйти', '/accounts/logout/')]

    if privilege_level == 1:
        average_score = get_apprentice_average_score(user_data.id)
        attendance_score = get_apprentice_attendance_score(user_data.id)

        tools.append(('Учебная группа', '/accounts/group/study/{0}'.format(user_data.study_group_id)))

        toolbox = toolbox_data(tools)
        return render(request, 'profiles/apprentice_page.html', {'profile_data': user_data,
                                                                 'average_score': average_score,
                                                                 'attendance_score': attendance_score,
                                                                 'toolbox': toolbox,
                                                                 'navbar': navbar_data(request)})
    elif privilege_level == 4:
        supervision_group = get_supervision_group(user_data.id)
        if supervision_group:
            tools.append(('Учебная группа', '/accounts/group/study/{0}'.format(supervision_group.id)))

        average_score = get_teacher_average_score(user_data.id)
        lessons_passed = get_all_teacher_lessons(user_data.id)

        toolbox = toolbox_data(tools)
        return render(request, 'profiles/teacher_page.html', {'profile_data': user_data,
                                                              'supervision_group': supervision_group,
                                                              'average_score': average_score,
                                                              'lessons_passed': lessons_passed,
                                                              'toolbox': toolbox,
                                                              'navbar': navbar_data(request)})

    elif privilege_level == 5:
        toolbox = toolbox_data(tools)
        return render(request, 'profiles/manager_page.html', {'profile_data': user_data,
                                                              'toolbox': toolbox,
                                                              'navbar': navbar_data(request)})


@login_required(login_url='/accounts/login/')
def profile(request, user_id=None):
    if user_id is not None:
        user_data = get_profile_data(user_id)
    else:
        user_data = get_profile_data(request.user.id)

    user_group = get_user_prior_group_number(user_id)
    tools = list()

    if user_group == 1:
        average_score = get_apprentice_average_score(user_data.id)
        attendance_score = get_apprentice_attendance_score(user_data.id)

        tools.append(('Учебная группа', '/accounts/group/study/{0}'.format(user_data.study_group_id)))

        if request.user.has_perm('accounts.change_apprentice'):
            tools.append(('Редактировать', 'edit'))

        toolbox = toolbox_data(tools)
        return render(request, 'profiles/apprentice_page.html', {'profile_data': user_data,
                                                                 'average_score': average_score,
                                                                 'attendance_score': attendance_score,
                                                                 'toolbox': toolbox,
                                                                 'navbar': navbar_data(request)})
    elif user_group == 4:
        if request.user.has_perm('accounts.change_teachers'):
            tools.append(('Редактировать', 'edit'))

        average_score = get_teacher_average_score(user_data.id)
        lessons_passed = get_all_teacher_lessons(user_data.id)

        supervision_group = get_supervision_group(user_data.id)
        if supervision_group:
            tools.append(('Учебная группа', '/accounts/group/study/{0}'.format(supervision_group.id)))

        toolbox = toolbox_data(tools)
        return render(request, 'profiles/teacher_page.html', {'profile_data': user_data,
                                                              'supervision_group': supervision_group,
                                                              'average_score': average_score,
                                                              'lessons_passed': lessons_passed,
                                                              'toolbox': toolbox,
                                                              'navbar': navbar_data(request)})
    elif user_group == 5:
        if request.user.has_perm('accounts.change_managers'):
            tools.append(('Редактировать', 'edit'))

        toolbox = toolbox_data(tools)
        return render(request, 'profiles/manager_page.html', {'profile_data': user_data,
                                                              'toolbox': toolbox,
                                                              'navbar': navbar_data(request)})


def edit_profile(request, user_id=None):
    if user_id is not None:
        user_data = get_profile_data(user_id)
    else:
        user_data = get_profile_data(request.user.id)

    user_group = get_user_prior_group_number(user_id)
    if request.user.id != user_id:
        if user_group == 1:
            if not request.user.has_perm('accounts.change_apprentice'):
                return HttpResponseForbidden()
        elif user_group == 4:
            if not request.user.has_perm('accounts.change_teachers'):
                return HttpResponseForbidden()
        elif user_group == 3:
            if not request.user.has_perm('accounts.change_teachers'):
                return HttpResponseForbidden()
        elif user_group == 2:
            if not request.user.has_perm('accounts.change_parents'):
                return HttpResponseForbidden()

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES)

        if form.is_valid():
            new_email = form.data.get('email')
            new_phone = form.data.get('phone')
            new_image = form.cleaned_data['profile_image']
            new_status = form.data.get('status')

            if user_data.email != new_email:
                user_data.email = new_email

            if user_data.phone != new_phone:
                user_data.phone = new_phone

            if new_image is not None:
                user_data.profile_picture = new_image

            user_data.save()
            return profile(request, user_id)

    if user_group == 1:
        return render(request, 'profiles/editors/apprentice_editor.html', {'profile_data': user_data,
                                                                           'navbar': navbar_data(request)})
    elif user_group == 4:
        return render(request, 'profiles/editors/teacher_editor.html', {'profile_data': user_data,
                                                                        'navbar': navbar_data(request)})
    elif user_group == 3:
        return None
    elif user_group == 2:
        return None
    elif user_group == 5:
        return render(request, 'profiles/editors/manager_editor.html', {'profile_data': user_data,
                                                                        'navbar': navbar_data(request)})


@permission_required('accounts.view_studygroups', raise_exception=True)
def view_all_groups(request):
    groups_data = get_all_groups()
    separated_study_groups = separate_study_groups(groups_data['study_groups'])

    return render(request, 'profiles/groups/all_groups.html', {'high_school_groups': separated_study_groups['high'],
                                                               'middle_school_groups': separated_study_groups['middle'],
                                                               'primary_school_groups': separated_study_groups[
                                                                   'primary'],
                                                               'creative_groups': groups_data['creative_groups'],
                                                               'navbar': navbar_data(request)})


@permission_required('accounts.view_studygroup', raise_exception=True)
def view_study_group(request, group_id):
    group_data = get_study_group_data(group_id)
    apprentices = get_study_group_apprentices(group_id)

    apprentices_grid = get_group_statistics(apprentices, group_data.id)

    if group_data.headman:
        headman = group_data.headman
        try:
            headman.__setattr__('stats', get_profile_statistics(headman.account_id))
        except AttributeError:
            headman.__setattr__('stats', ('N/A', 'N/A', 'N/A'))
    else:
        headman = None

    if group_data.methodist:
        methodist = group_data.methodist
        try:
            methodist.__setattr__('stats', get_profile_statistics(methodist.account_id))
        except AttributeError:
            methodist.__setattr__('stats', ('N/A', 'N/A', 'N/A'))
    else:
        methodist = None

    if group_data.supervisor:
        supervisor = group_data.supervisor
        try:
            supervisor.__setattr__('stats', get_profile_statistics(supervisor.account_id))
        except AttributeError:
            supervisor.__setattr__('stats', ('N/A', 'N/A', 'N/A'))
    else:
        supervisor = None

    toolbox = toolbox_data([('Все группы', '../../all'),
                            ('Статистика', '/statistics/groups/{0}'.format(group_id)),
                            ('Редактировать', 'edit/')])

    return render(request, 'profiles/groups/group_page.html', {'group_data': group_data,
                                                               'headman': headman,
                                                               'methodist': methodist,
                                                               'supervisor': supervisor,
                                                               'first_column': apprentices_grid[0],
                                                               'second_column': apprentices_grid[1],
                                                               'third_column': apprentices_grid[2],
                                                               'toolbox': toolbox,
                                                               'navbar': navbar_data(request)})


@permission_required('accounts.change_studygroup', raise_exception=True)
def edit_study_group(request, group_id):
    group_data = get_study_group_data(group_id)
    apprentices = get_study_group_apprentices(group_id)

    if request.method == 'POST':
        form = GroupEditForm(request.POST)

        new_specialisation = form.data.get('specialisation')
        new_supervisor = form.data.get('supervisor')
        new_headman = form.data.get('headman')
        new_methodist = form.data.get('methodist')

        set_study_group_settings(group_data, new_specialisation, new_headman, new_supervisor, new_methodist)

    available_settings = get_available_study_group_settings(group_data)

    return render(request,
                  'profiles/editors/group_editor.html',
                  {'group_data': group_data,
                   'available_supervisors': available_settings['available_supervisors'],
                   'available_specialisations': available_settings['available_specialisations'],
                   'available_methodists': available_settings['available_methodists'],
                   'apprentices': apprentices,
                   'navbar': navbar_data(request)})
