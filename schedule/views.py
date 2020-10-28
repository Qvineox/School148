from django.shortcuts import render
from schedule.services import *
from django.shortcuts import render

from schedule.services import *


def timeline(request):
    return render(request, 'schedule/timeline.html')


def create_week_lessons(request):
    start_week_replenish()
    return render(request, 'schedule/timeline.html')
