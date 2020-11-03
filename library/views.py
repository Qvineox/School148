from accounts.services import get_profile_data
from django.shortcuts import render
from library.models import LoanReceipts


def show_library(request):
    books = LoanReceipts.objects.all()
    person_data = navbar_data(request)
    return render(request, 'library/apprentice_library_home.html', {'books': books, 'person_data': person_data})


def navbar_data(request):
    data = get_profile_data(request.user.id)

    data = {
        'first_name': data.first_name,
        'second_name': data.second_name,
        'last_name': data.last_name,
        'id': data.account_id
    }

    return data


