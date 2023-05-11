from collections import namedtuple

from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render

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

    return render(request, 'customers/pages/customermenu.html', {'table': table,
                                                                 'categories': categories,
                                                                 'uncategorizedItems': uncategorizedItems
                                                                 })
