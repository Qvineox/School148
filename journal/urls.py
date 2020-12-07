from django.urls import path

from journal import views

urlpatterns = [
    path('', views.show_journal, name='journal_page'),
    path('lesson/<int:lesson_id>/panel', views.lesson_panel, name='lesson panel'),
]
