from django.shortcuts import render, redirect
from home.views import navbar_data
from library.models import Books, LoanReceipts
from journal.models import Disciples
from accounts.services import get_profile_data, get_profile_from_user
from library.forms import BookAddForm

def show_library(request):
    lib_books = Books.objects.all()
    bor_books = LoanReceipts.objects.filter(borrower_id=request.user.id)
    person_data = navbar_data(request)
    return render(request, 'library/new_lib.html',
                  {'all_books': lib_books,
                   'person_data': person_data,
                   'navbar': person_data,
                   'my_books': bor_books
                   })


def book_borrow_page(request, pk):
    lib_book = Books.objects.get(ISBN_number=pk)
    disciples = Disciples.objects.all()
    person_data = navbar_data(request)
    if request.method == 'POST':
        form = BookAddForm(request.POST)
        print(form)
        print(form.errors)
        if form.is_valid():
            
                form.save()
                return redirect('library_page')
    else:
        print(pk)
        form = BookAddForm(initial={'book': pk, 'borrower': request.user})

    return render(request, 'library/book_detail.html',
                  {
                      'book_detail': lib_book,
                      'navbar': person_data,
                      'predmety': disciples,
                      'add_book_form': form
                   }
                  )
