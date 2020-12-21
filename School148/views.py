from datetime import timedelta

from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.utils import timezone

from accounts.services import get_user_prior_group_number
from home.views import navbar_data
from schedule.services import start_interval_replenish, start_interval_cleanup, start_full_cleanup


def settings_page(request):
    if get_user_prior_group_number(request.user.id) < 5:
        return HttpResponseForbidden()

    if request.GET.get('fill_schedule'):
        command = request.GET.get('fill_schedule')
        today = timezone.now().date()
        if command == 'today':
            start_interval_replenish(today)
        elif command == 'week':
            week_start = today - timedelta(days=today.weekday())
            week_end = week_start + timedelta(days=6)
            start_interval_replenish(week_start, week_end)
        elif command == 'month':
            month_start = today.replace(day=1)
            next_month = today.replace(day=28) + timedelta(days=4)
            month_end = next_month - timedelta(days=next_month.day)

            start_interval_replenish(month_start, month_end)
        elif command == 'tomorrow':
            start_interval_replenish(today + timedelta(days=1))
        elif command == 'next_week':
            week_start = today - timedelta(days=today.weekday()) + timedelta(days=6)
            week_end = week_start + timedelta(days=7)
            start_interval_replenish(week_start, week_end)
        elif command == 'next_month':
            next_month_start = (today.replace(day=1) + timedelta(days=32)).replace(day=1)
            next_month = next_month_start.replace(day=28) + timedelta(days=4)
            next_month_end = next_month - timedelta(days=next_month.day)

            start_interval_replenish(next_month_start, next_month_end)
        return redirect('/settings/')

    if request.GET.get('clear_schedule'):
        command = request.GET.get('clear_schedule')
        today = timezone.now().date()
        if command == 'today':
            start_interval_cleanup(today)
        elif command == 'week':
            week_start = today - timedelta(days=today.weekday())
            week_end = week_start + timedelta(days=6)

            start_interval_cleanup(week_start, week_end)
        elif command == 'month':
            month_start = today.replace(day=1)
            next_month = today.replace(day=28) + timedelta(days=4)
            month_end = next_month - timedelta(days=next_month.day)

            start_interval_cleanup(month_start, month_end)
        elif command == 'full':
            start_full_cleanup()

        return redirect('/settings/')

    if request.GET.get('load_schedule'):
        return redirect('/settings/')

    return render(request, 'settings/settings_page.html', {'navbar': navbar_data(request)})
