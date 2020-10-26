from django.urls import path

from accounts import views

urlpatterns = [
    path('statistics/', views.basic_statistics, name='statistics')
]