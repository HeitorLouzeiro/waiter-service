from collections import namedtuple

from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render

from waiter.models import Task

from .models import Category, Commands, ItemMenu, Table

# Create your views here.


def home(request):
    template_name = 'customers/pages/home.html'
    return render(request, template_name)


def clientDesk(request, slug):
    table = get_object_or_404(Table, slug=slug)
    Requests = namedtuple("Requests", ['Ready', 'in_preparation', 'Delivered'])
    requests = None
    try:
        commands = Commands.objects.get(Table=table, status='open')
        requestsReady = commands.itemorder_set.filter(status='ready')
        requestsInPreparation = commands.itemorder_set.filter(
            status='preparation')
        requestsDelivered = commands.itemorder_set.filter(status='delivered')
        requests = Requests(
            requestsReady, requestsInPreparation, requestsDelivered)

    except Commands.DoesNotExist:
        commands = None
    return render(request,
                  'customers/pages/clientDesk.html',
                  {'table': table, 'commands': commands, 'requests': requests})


def customermenu(request, slug):
    table = get_object_or_404(Table, slug=slug)
    categories = Category.objects. \
        annotate(active=Count('itemmenu',
                 filter=Q(itemmenu__active=True))). \
        filter(active__gt=0)
    uncategorizedItems = ItemMenu.objects.filter(
        category__isnull=True, active=True)

    return render(request, 'customers/pages/customermenu.html',
                  {'table': table, 'categories': categories,
                   'uncategorizedItems': uncategorizedItems
                   })


def requestService(request, slug):
    table = get_object_or_404(Table, slug=slug)
    # There is already an open command for the table that made the request

    # Check if there is a pending service request for the table
    # except delivery

    try:
        commands = Commands.objects.get(Table=table, status='open')
    except Commands.DoesNotExist:
        commands = None

    if commands:
        try:
            task = Task.objects.get(
                ~Q(type='deliver'), table=table, status='pending')
            if task.type != 'prim_attendance':
                task.type = 'service'
                task.save()

        except Task.DoesNotExist:
            task = Task.objects.create(
                type='service', table=table
            )
    else:

        # in this case, there is no open command for the table
        # open a new command for the table

        commands = Commands.objects.create(Table=table)
        # create a new first call task for the table
        task = Task.objects.create(
            type='prim_attendance', table=table
        )
    return render(request, 'customers/pages/requestService.html',
                  {'table': table, 'commands': commands, 'task': task
                   })


def requestClose(request, slug):
    table = get_object_or_404(Table, slug=slug)
    try:
        task = Task.objects.get(
            ~Q(type='delivery'), table=table, status='pending')
        if task.type != 'prim_attendance':
            task.type = 'closed'
            task.save()

    except Task.DoesNotExist:
        task = Task.objects.create(
            type='closed', table=table)
    return render(request, 'customers/pages/requestService.html',
                  {'table': table, 'task': task})
