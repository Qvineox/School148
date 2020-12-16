from django.shortcuts import render

from home.views import navbar_data


# страница главной статистики
def overall_statistics(request):
    return render(request, 'statistics/overall_statistics.html', {'navbar': navbar_data(request)})
