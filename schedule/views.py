from django.shortcuts import render
from schedule.services import *
from django.shortcuts import render

from schedule.services import *


def timeline(request):
    return render(request, 'schedule/timeline.html')


def create_week_lessons(request):
    date_time_str = '2020-11-01'
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')
    start_week_replenish(date_time_obj)
    return timeline(request)
