from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import get_random_string


# Create your models here.
class Table(models.Model):

    number = models.CharField(max_length=3, unique=True)
    slug = models.SlugField(max_length=8, blank=True, unique=True)

    def __str__(self):
        return f"Table {self.number}"

    def save(self, *args, **kwargs):
        self.slug_save()
        super(Table, self).save(*args, **kwargs)

    def slug_save(self):
        if not self.slug:
            self.slug = get_random_string(8)
            slug_is_wrong = True
            while slug_is_wrong:
                slug_is_wrong = False
                other_objs_with_slug = type(
                    self).objects.filter(slug=self.slug)
                if len(other_objs_with_slug) > 0:
                    slug_is_wrong = True
                if slug_is_wrong:
                    self.slug = get_random_string(8)

    def get_absolute_url(self):
        return reverse("customers:clientDesk", args=(self.slug,))

    def get_menu_url(self):
        return reverse("customers:customermenu", args=(self.slug,))


class Commands(models.Model):
    OPCOES_STATUS = (
        ('open', 'Open'),
        ('close', 'Close')
    )
    code = models.SlugField(max_length=8, blank=True, unique=True)
    Table = models.ForeignKey(Table, null=True, on_delete=models.SET_NULL)
    opening = models.DateTimeField(auto_now_add=True)
    closed = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=7, choices=OPCOES_STATUS, default='open')
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        self.slug_save()
        super(Commands, self).save(*args, **kwargs)

    def slug_save(self):
        if not self.code:
            self.code = get_random_string(8)
            slug_is_wrong = True
            while slug_is_wrong:
                slug_is_wrong = False
                other_objs_with_slug = type(
                    self).objects.filter(code=self.code)
                if len(other_objs_with_slug) > 0:
                    slug_is_wrong = True
                if slug_is_wrong:
                    self.code = get_random_string(8)

    def update_total(self):
        items = ItemOrder.objects.filter(commands=self)
        new_total = 0.00
        for item in items:
            new_total += float(item.price)
        self.amount = new_total
        self.save()

    def __str__(self):
        return f"Command {self.code} - Table {self.Table.number}"


class Category(models.Model):
    name = models.CharField(max_length=55)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0, blank=True)

    class Meta:
        ordering = ('order', 'name')

    def __str__(self):
        return self.name


class ItemMenu(models.Model):
    item = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    active = models.BooleanField(default=True)
    needs_preparation = models.BooleanField(default=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.item


class ItemOrder(models.Model):
    OPCOES_STATUS = (
        ('preparation', 'In preparation'),
        ('ready', 'Ready'),
        ('delivered', 'Delivered'),
    )
    item = models.ForeignKey(ItemMenu, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    commands = models.ForeignKey(Commands, on_delete=models.PROTECT)
    status = models.CharField(
        max_length=11, choices=OPCOES_STATUS, default="preparation")
    obs = models.TextField(blank=True)
    preparation_time = models.DateTimeField(auto_now_add=True)
    delivery_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('preparation_time', 'item')

    def order_ready(self):
        if self.status == 'preparation':
            self.status = 'ready'
            self.save()

    def deliver_order(self):
        self.status = 'delivered'
        self.delivery_time = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.commands.code} - {self.item.item} -  {self.status}"
