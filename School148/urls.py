from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from rest_framework.authtoken import views as rest_views

from School148 import settings, views
from accounts import views as accounts

urlpatterns = [
    path('', accounts.account_login),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('home/', include('home.urls')),
    path('schedule/', include('schedule.urls')),
    path('journal/', include('journal.urls')),
    path('library/', include('library.urls')),
    path('statistics/', include('statistic.urls')),
    path('settings/', views.settings_page, name='settings'),
    path('api/', include('api.urls', namespace='api')),
    path('api-token-auth/', rest_views.obtain_auth_token, name='api-token-auth'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
