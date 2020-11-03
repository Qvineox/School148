from django.urls import path

from library import views

urlpatterns = [
    path('', views.show_library, name='library_page'),
]
