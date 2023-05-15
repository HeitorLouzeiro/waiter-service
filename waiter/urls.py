from django.urls import path

from . import views

app_name = 'waiter'

urlpatterns = [
    path('', views.panelView, name='panelview'),
    path('perform-service/<int:task_id>/',
         views.performService, name='performService'),
    path('new-order/', views.newOrder, name='newOrder'),
    path('new-order/<slug:table_slug>/', views.newOrder, name='newOrderTable'),
    path('confirm-order/', views.confirmOrder, name='confirmOrder'),
    path('create-order/', views.createOrder, name='createOrder'),
    path('status-order/<slug:delivery_id>',
         views.statusOrder, name='statusOrder'),
    path('perform-service-close/<slug:task_id>',
         views.performServiceClose, name='performServiceClose'),
]
