from django.shortcuts import render, redirect
from home.views import navbar_data
from library.models import Books, LoanReceipts
from journal.models import Disciples
from library.forms import BookAddForm



def show_library(request):
    lib_books = list(Books.objects.all())
    bor_books = list(LoanReceipts.objects.filter(borrower_id=request.user.id))
    # copy_lib_books = lib_books
    # isbn_arr_bor = []
    # for bor_book in bor_books:
    #     isbn_arr_bor.append(bor_book.book_id)
    # for counter, copy_lib_books in enumerate(copy_lib_books):
    #     print(counter)
    #     if copy_lib_books.ISBN_number in isbn_arr_bor:
    #         print(copy_lib_books.ISBN_number)
    #         copy_lib_books.pop(counter - 1)
    for bor_book in bor_books:
        for lib_book in lib_books:
            if bor_book.book.ISBN_number == lib_book.ISBN_number:
                lib_books.pop(lib_books.index(lib_book))
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
        if form.is_valid():
            form.save()
            return redirect('library_page')
    else:

        form = BookAddForm(initial={'book': pk, 'borrower': request.user})

    return render(request, 'library/book_detail.html',
                  {
                      'book_detail': lib_book,
                      'navbar': person_data,
                      'predmety': disciples,
                      'add_book_form': form
                   })


def return_book_page(request, fk):
    bor_book = LoanReceipts.objects.get(book_id=fk)
    person_data = navbar_data(request)
    if request.method == 'POST':
        bor_book.delete()
        return redirect('library_page')

    return render(request, 'library/return_book_page.html',
                  {
                      'book_detail': bor_book,
                      'navbar': person_data,


                  })