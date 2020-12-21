from django.urls import path

from library import views

urlpatterns = [
    path('', views.show_library, name='library_page'),
    path("<int:pk>/", views.book_borrow_page, name='borrow_book_page')
]
