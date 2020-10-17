from django.urls import path

from accounts import views

urlpatterns = [
    path('login/', views.site_login, name='login'),
]
