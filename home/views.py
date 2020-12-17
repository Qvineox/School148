from django.contrib.auth.decorators import login_required
from django.shortcuts import render

import accounts.services as account_services
from home.services import get_apprentice_home_data


@login_required
def home(request):
    home_apprentice_data = get_apprentice_home_data(request.user.id)

    return render(request, 'home/apprentice_home.html', {'navbar': navbar_data(request),
                                                         'lessons': home_apprentice_data['lessons'],
                                                         'pretext': home_apprentice_data['pretext'],
                                                         'date': home_apprentice_data['date'],
                                                         'homeworks': home_apprentice_data['homeworks'],
                                                         'marks': home_apprentice_data['marks']})


def navbar_data(request):
    data = account_services.get_profile_data(request.user.id)

    data = {
        'first_name': data.first_name,
        'second_name': data.second_name,
        'last_name': data.last_name,
        'id': data.id
    }

    return data


class Tool(object):
    def __init__(self, title, link):
        self.title = title
        self.link = link


def toolbox_data(tools_list):
    toolbox = []
    for item in tools_list:
        toolbox.append(Tool(item[0], item[1]))

    return toolbox
