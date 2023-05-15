from collections import namedtuple

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import redirect, render

from customers.models import Category, Commands, ItemMenu, ItemOrder, Table

from .models import Delivery, Task


# Create your views here.
@login_required(login_url='accounts:loginUser', redirect_field_name='next')
def panelView(request):
    template = 'waiter/pages/panel.html'

    deliveries = Delivery.objects.filter(~Q(order__status="delivered"))
    prim_attendances = Task.objects.filter(
        type='prim_attendance', status="pending")
    services = Task.objects.filter(type='service', status="pending")
    closures = Task.objects.filter(type='closed', status="pending")
    qtd_services = prim_attendances.count() + services.count()

    context = {'deliveries': deliveries,
               'prim_attendances': prim_attendances,
               'services': services,
               'closures': closures,
               'qtd_services': qtd_services,
               }

    return render(request, template, context)


@login_required(login_url='accounts:loginUser', redirect_field_name='next')
def performService(request, task_id):
    waiter = request.user
    task = Task.objects.get(id=task_id)
    task.attend_task(waiter)

    return redirect('waiter:newOrderTable', table_slug=task.table.slug)


@login_required(login_url='accounts:loginUser', redirect_field_name='next')
def newOrder(request, table_slug=None):
    template = 'waiter/pages/waitermenu.html'
    table = None
    if table_slug is not None:
        table = Table.objects.get(slug=table_slug)

    categories = Category.objects. \
        annotate(active=Count('itemmenu',
                              filter=Q(itemmenu__active=True))). \
        filter(active__gt=0)

    uncategorizedItems = ItemMenu.objects.filter(
        category__isnull=True, active=True)

    context = {'table': table,
               'categories': categories,
               'uncategorizedItems': uncategorizedItems
               }
    return render(request, template, context)


def confirmOrder(request):
    Order = namedtuple('Order', ['id', 'item', 'amount'])
    orders = []
    numTable = int(request.POST.get('num_mesa'))
    table = Table.objects.get(number=numTable)
    for item_id, amount in request.POST.items():
        try:
            id = int(item_id)
        except ValueError:
            pass
        else:
            if int(amount) > 0:
                orders.append(
                    Order(id, ItemMenu.objects.get(id=id), int(amount)))

    return render(request, 'waiter/pages/confirmorder.html', {'orders': orders,
                                                              'table': table})


def createOrder(request):
    orderDict = request.POST.copy()
    numTable = int(orderDict.get('num_mesa'))
    table = Table.objects.get(number=numTable)

    commands = Commands.objects.get(Table=table, status='open')
    del orderDict['num_mesa']
    del orderDict['csrfmiddlewaretoken']

    for item_id, amount in orderDict.items():
        itemmenu = ItemMenu.objects.get(id=int(item_id))
        for i in range(int(amount)):
            newOder = ItemOrder(
                item=itemmenu,
                price=float(itemmenu.price),
                commands=commands,
                status='preparation' if itemmenu.needs_preparation else 'ready'
            )
            newOder.save()
    commands.update_total()

    return redirect('waiter:panelview')


def statusOrder(request, delivery_id):
    delivery = Delivery.objects.get(id=delivery_id)
    order = ItemOrder.objects.get(id=delivery.order.id)
    if order.status == 'preparation':
        order.order_ready()
    elif order.status == 'ready':
        order.deliver_order()

    return redirect('waiter:panelview')
