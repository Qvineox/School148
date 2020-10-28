from django.contrib.auth.decorators import login_required
from django.shortcuts import render

import accounts.services as account_services
import journal.services as journal_services


# Create your views here.

def navbar_data(request):
    data = account_services.get_profile_data(request.user.id)

    data = {
        'first_name': data.first_name,
        'second_name': data.second_name,
        'last_name': data.last_name,
        'id': data.id
    }

    return data


@login_required
def home(request):
    data = {}
    school_profile = account_services.get_profile_from_user(request.user.id)

    print(school_profile.study_group.id)
    # data = {
    #     'lesson_cards': journal_services.get_lessons_for_study_group(),
    # }

    data.update(navbar_data(request))
    return render(request, 'home/apprentice_home.html', data)
