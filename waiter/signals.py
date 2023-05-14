from django.db.models.signals import post_save
from django.dispatch import receiver

from customers.models import ItemOrder

from .models import Delivery, Task


@receiver(post_save, sender=ItemOrder)
def create_delivery(sender, instance, created, **kwargs):
    if created and instance.status == 'preparation':
        task = Task.objects.latest('hr_creation')
        if task:
            delivery = Delivery(order=instance, task=task)
            delivery.save()
