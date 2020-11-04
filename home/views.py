from django.contrib.auth.decorators import login_required
from django.shortcuts import render

import accounts.services as account_services


# Create your views here.


@login_required
def home(request):
    return render(request, 'home/apprentice_home.html', {'navbar': navbar_data(request)})


def navbar_data(request):
    data = account_services.get_profile_data(request.user.id)

    data = {
        'first_name': data.first_name,
        'second_name': data.second_name,
        'last_name': data.last_name,
        'id': data.id
    }

    return data
