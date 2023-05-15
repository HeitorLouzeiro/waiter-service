from django.conf import settings
from django.db import models
from django.utils import timezone

from customers.models import ItemOrder, Table


class Task(models.Model):

    OPTIONS_TYPE = (
        ('prim_attendance', 'First Call'),
        ('service', 'Service'),
        ('closed', 'Closed'),
        ('deliver', 'Deliver')
    )

    STATUS_OPTIONS = (
        ('pending', 'Pending'),
        ('done', 'Done'),
    )

    type = models.CharField(max_length=16, choices=OPTIONS_TYPE)
    waiter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        null=True, blank=True)
    status = models.CharField(
        max_length=9, choices=STATUS_OPTIONS, default='pending')
    hr_creation = models.DateTimeField(auto_now_add=True)
    hr_service = models.DateTimeField(null=True, blank=True)
    table = models.ForeignKey(Table, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.get_type_display()} on table {self.table.number}"

    def attend_task(self, waiter):
        self.waiter = waiter
        self.status = 'done'
        self.hr_service = timezone.now()
        self.save()


class Delivery(models.Model):
    order = models.OneToOneField(ItemOrder, on_delete=models.CASCADE)

    def __str__(self):
        return f"Delivery of {self.order.item.item} on table \
                    {self.order.commands.Table.number} \
                        status {self.order.status}"
