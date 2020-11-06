from django.shortcuts import render
from home.views import navbar_data
from library.models import Books, LoanReceipts


def show_library(request):
    lib_books = Books.objects.all()
    bor_books = LoanReceipts.objects.all()
    person_data = navbar_data(request)
    return render(request, 'library/apprentice_library_home.html',
                  {'all_books': lib_books, 'person_data': person_data, 'navbar': person_data, 'my_books': bor_books})


