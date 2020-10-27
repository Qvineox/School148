from django.urls import path

from accounts import views

urlpatterns = [
    path('login/', views.account_login, name='login'),
    path('preregistration/', views.account_preregister, name='preregistration'),
    path('registration/', views.account_register, name='registration'),
    path('home/', views.home, name='home'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
]
