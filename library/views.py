from django.shortcuts import render

from home.views import navbar_data
from library.models import LoanReceipts


def show_library(request):
    books = LoanReceipts.objects.all()
    person_data = navbar_data(request)
    return render(request, 'library/apprentice_library_home.html',
                  {'books': books, 'person_data': person_data, 'navbar': person_data})
