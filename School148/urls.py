"""School148 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from accounts import views as accounts
from School148 import settings, views

urlpatterns = [
    path('', accounts.account_login),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('home/', include('home.urls')),
    path('schedule/', include('schedule.urls')),
    path('journal/', include('journal.urls')),
    path('library/', include('library.urls')),
    path('statistics/', include('statistic.urls')),
    path('settings/', views.settings_page, name='settings')
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
