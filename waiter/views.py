from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Task


# Create your views here.
@login_required(login_url='accounts:loginUser', redirect_field_name='next')
def panelView(request):
    template = 'waiter/pages/panel.html'

    deliveries = Task.objects.filter(type='deliver')
    prim_attendances = Task.objects.filter(type='prim_attendance')
    services = Task.objects.filter(type='service')
    closures = Task.objects.filter(type='closed')
    qtd_services = prim_attendances.count() + services.count()

    context = {'deliveries': deliveries,
               'prim_attendances': prim_attendances,
               'services': services,
               'closures': closures,
               'qtd_services': qtd_services,
               }

    return render(request, template, context)
