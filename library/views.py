from django.shortcuts import render, redirect
from home.views import navbar_data
from library.models import Books, LoanReceipts
from library.forms import BookAddForm
from accounts.models import Apprentices


def show_library(request):
    lib_books = Books.objects.all()
    bor_books = LoanReceipts.objects.all()
    person_data = navbar_data(request)
    print(Apprentices.pk)
    if request.method == 'POST':

        form = BookAddForm(request.POST)

        # print(form.borrower)
        print(form.errors)
        if form.is_valid():

            form.save()
            return redirect('library/apprentice_library_home.html')
    else:
        form = BookAddForm()

    return render(request, 'library/apprentice_library_home.html',
                  {'all_books': lib_books,
                   'person_data': person_data,
                   'navbar': person_data,
                   'my_books': bor_books,
                   'add_book_form': form
                   })
