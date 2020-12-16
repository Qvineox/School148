from django.urls import path

from statistic import views

urlpatterns = [
    path('', views.overall_statistics, name='statistics main page')
]
