from django.urls import path

from library import views

urlpatterns = [
    path('', views.show_library, name='library_page'),
    path("borrrow/<int:pk>/", views.book_borrow_page, name='borrow_book_page'),
    path("returne/<int:fk>/", views.return_book_page, name='return_book_page')
]
