from django.shortcuts import render

# Create your views here.
from home.views import navbar_data
from journal.services import *


def show_journal(request):
    return render(request, 'journal/apprentice_journal.html',
                  {'navbar': navbar_data(request), 'lessons': get_schedule_for_user(request.user)})
