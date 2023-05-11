from django.urls import path

from . import views

app_name = 'customers'

urlpatterns = [
    path('', views.home, name='home'),
    path('customers/table/<slug:slug>/', views.clientDesk, name='clientDesk'),
    path('customermenu/<slug:slug>/', views.customermenu, name='customermenu'),
    path('request-service/<slug:slug>/',
         views.requestService, name='requestService'),
    path('request-close/<slug:slug>/', views.requestClose, name='requestClose'),
]
