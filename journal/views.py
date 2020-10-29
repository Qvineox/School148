from django.shortcuts import render


# Create your views here.
from accounts.services import get_profile_data


def show_journal(request):
    return render(request, 'journal/apprentice_journal.html', navbar_data(request))


def navbar_data(request):
    data = get_profile_data(request.user.id)

    data = {
        'first_name': data.first_name,
        'second_name': data.second_name,
        'last_name': data.last_name,
        'id': data.id
    }

    return data
