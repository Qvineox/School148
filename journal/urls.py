from django.urls import path

from journal import views

urlpatterns = [
    path('', views.show_journal, name='journal page'),
    path('marks', views.show_marks, name='marks page'),
    path('lessons/history', views.lesson_history, name='lessons history'),
    path('lessons/<int:lesson_id>/panel', views.lesson_panel, name='lesson panel'),
]
