from django.shortcuts import render
from schedule.services import *
from django.shortcuts import render

from schedule.services import *


def timeline(request):
    return render(request, 'schedule/timeline.html')


def create_week_lessons(request):
    print(start_week_replenish())
    return timeline(request)
