from django.urls import path

from journal import views

urlpatterns = [
    path('', views.show_journal, name='journal_page'),
]
