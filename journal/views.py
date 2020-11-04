from django.shortcuts import render


# Create your views here.
from accounts.services import get_profile_data
from home.views import navbar_data
from journal.services import *


def show_journal(request):
    data = navbar_data(request)

    data.update(get_schedule_for_user(request.user))
    return render(request, 'journal/apprentice_journal.html', {'navbar': navbar_data(request)})


