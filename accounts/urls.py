from django.urls import path

from accounts import views

urlpatterns = [
    path('login/', views.account_login, name='login'),
    path('preregistration/', views.account_preregister, name='preregistration'),
    path('registration/', views.account_register, name='registration'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('profile/<int:user_id>/edit', views.edit_profile, name='edit profile'),
    path('group/all/', views.view_all_groups, name='view all groups'),
    path('group/<int:group_id>/', views.view_group, name='view group'),
]
