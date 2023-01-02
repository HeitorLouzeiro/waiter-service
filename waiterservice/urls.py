from django.urls import path

from . import views

app_name = 'waiterservice'

urlpatterns = [
    path('', views.home, name='home'),
]
