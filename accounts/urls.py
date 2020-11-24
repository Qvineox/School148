from django.urls import path

from accounts import views

urlpatterns = [
    path('login/', views.account_login, name='login'),
    path('preregistration/', views.account_preregister, name='preregistration'),
    path('registration/', views.account_register, name='registration'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('profile/<int:user_id>/edit', views.edit_profile, name='edit profile'),
    path('group/all/', views.view_all_groups, name='view all groups'),
    path('group/study/<int:group_id>/', views.view_study_group, name='view study group'),
    path('group/study/<int:group_id>/edit/', views.edit_study_group, name='edit study group'),
    # path('group/creative/<int:group_id>/', views.view_creative_group, name='view creative group'),
    # path('group/project/<int:group_id>/', views.view_project_group, name='view project group'),
]
