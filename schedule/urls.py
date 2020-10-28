from django.urls import path

from schedule import views

urlpatterns = [
    path('', views.timeline, name='timeline'),
    path('fill_week/', views.create_week_lessons, name='fill week')
]
