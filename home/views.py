from django.contrib.auth.decorators import login_required
from django.shortcuts import render

import accounts.services as account_services
from home.services import get_apprentice_home_data, get_teacher_home_data


@login_required(login_url='/accounts/login/')
def home(request):
    privilege_level = account_services.get_user_prior_group_number(request.user.id)

    # уровень ученика
    if privilege_level == 1:
        home_data = get_apprentice_home_data(request.user.id)
        return render(request, 'home/apprentice_home.html', {'navbar': navbar_data(request),
                                                             'lessons': home_data['lessons'],
                                                             'pretext': home_data['pretext'],
                                                             'date': home_data['date'],
                                                             'homeworks': home_data['homeworks'],
                                                             'marks': home_data['marks']})

    # уровень преподавателя
    elif privilege_level == 4:
        home_data = get_teacher_home_data(request.user.id)
        return render(request, 'home/teacher_home.html', {'navbar': navbar_data(request),
                                                          'lessons': home_data['lessons'],
                                                          'pretext': home_data['pretext'],
                                                          'date': home_data['date'],
                                                          'homeworks': home_data['homeworks'],
                                                          'marks': home_data['marks']})

    else:
        home_data = None


def navbar_data(request):
    data = account_services.get_profile_data(request.user.id)

    data = {
        'first_name': data.first_name,
        'second_name': data.second_name,
        'last_name': data.last_name,
        'privilege': account_services.get_user_prior_group_number(request.user.id),
        'id': data.id
    }

    return data


class Tool(object):
    def __init__(self, title, link):
        self.title = title
        self.link = link


def toolbox_data(tools_list):
    toolbox = []
    # сортировка инстурментов-пузырьков по длине
    tools_list.sort(key=lambda t: len(t[0]), reverse=True)

    for item in tools_list:
        toolbox.append(Tool(item[0], item[1]))

    return toolbox
