from django.db.models.signals import post_save
from django.dispatch import receiver

from customers.models import ItemOrder

from .models import Delivery


@receiver(post_save, sender=ItemOrder)
def create_delivery(sender, instance, created, **kwargs):
    if created and instance.status == 'preparation':
        delivery = Delivery(order=instance)
        delivery.save()
