from django.contrib.auth.decorators import login_required
from django.shortcuts import render

import accounts.services as account_services
from home.services import get_homepage_lessons


@login_required
def home(request):
    lessons, pretext, date = get_homepage_lessons(request.user.id)
    return render(request, 'home/apprentice_home.html', {'navbar': navbar_data(request),
                                                         'lessons': lessons,
                                                         'pretext': pretext,
                                                         'date': date})


def navbar_data(request):
    data = account_services.get_profile_data(request.user.id)

    data = {
        'first_name': data.first_name,
        'second_name': data.second_name,
        'last_name': data.last_name,
        'id': data.id
    }

    return data
