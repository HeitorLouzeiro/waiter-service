from django.urls import path

from . import views

app_name = 'waiter'

urlpatterns = [
    path('', views.panelView, name='panelview'),
]
