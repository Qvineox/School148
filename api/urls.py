from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from .views import *

app_name = 'api'
urlpatterns = [
    path('test/', Test.as_view(), name='test'),
    path('user_auth/', UserAuthView.as_view(), name='user_auth'),
    path('token/', obtain_auth_token, name='obtain_token'),
    path('week_lessons/', WeekLessonsView.as_view(), name='view_week_lessons'),
    path('profile/<int:profile_id>', ProfilesView.as_view(), name='view_profile'),
    path('future_homeworks/', FutureHomeworks.as_view(), name='view_homework'),
    path('all_marks/', MarksView.as_view(), name='view_marks'),
    path('homework/<int:homework_id>', FutureHomeworks.as_view(), name='view_homework'),
]
