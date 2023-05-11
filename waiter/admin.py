from django.contrib import admin

from .models import Delivery, Task

# Register your models here.
admin.site.register(Task)
admin.site.register(Delivery)
