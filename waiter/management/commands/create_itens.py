# hello.py
from django.core.management.base import BaseCommand

from customers.models import Category, ItemMenu, Table


def createTables():
    tables = [1, 2, 3, 4, 5]
    slug = "table"

    for table in tables:
        slug_with_number = slug + str(table)
        Table.objects.create(number=table, slug=slug_with_number)
    print("Tables created")


def createCategory():
    categories = ['Burgers', 'Pizzas', 'Pasteis', 'Drinks']
    for category in categories:
        Category.objects.create(name=category)
    print("Categories created")


def createItemsMenu():
    category_drinks = Category.objects.get(name='Drinks')
    category_burgers = Category.objects.get(name='Burgers')
    category_pizzas = Category.objects.get(name='Pizzas')
    category_pasteis = Category.objects.get(name='Pasteis')

    itemMenu = [
        {
            'name': 'Agua',
            'category': category_drinks,
            'price': '2.00',
            'active': True,
            'needs_preparation': False,
            'description': 'Agua com gas'
        },
        {
            'name': 'Coca-Cola',
            'category': category_drinks,
            'price': '3.00',
            'active': True,
            'needs_preparation': False,
            'description': 'Coca-Cola 350ml'
        },
        {
            'name': 'Guarana',
            'category': category_drinks,
            'price': '3.00',
            'active': True,
            'needs_preparation': False,
        },
        {
            'name': 'Pizza marguerita',
            'category': category_pizzas,
            'price': '20.00',
            'active': True,
            'needs_preparation': True,
        },
        {
            'name': 'Pizza calabresa',
            'category': category_pizzas,
            'price': '20.00',
            'active': True,
            'needs_preparation': True,
        },
        {
            'name': 'Pastel de carne',
            'category': category_pasteis,
            'price': '5.00',
            'active': True,
            'needs_preparation': True,
        },
        {
            'name': 'Pastel de queijo',
            'category': category_pasteis,
            'price': '5.00',
            'active': True,
            'needs_preparation': True,
        },
        {
            'name': 'Burger de carne',
            'category': category_burgers,
            'price': '10.00',
            'active': True,
            'needs_preparation': True,
        },
        {
            'name': 'Burger de frango',
            'category': category_burgers,
            'price': '10.00',
            'active': True,
            'needs_preparation': True,
        },

    ]

    for item in itemMenu:
        if 'description' in item:
            description = item['description']
        else:
            description = ''

        ItemMenu.objects.create(
            item=item['name'],
            category=item['category'],
            price=item['price'],
            active=item['active'],
            needs_preparation=item['needs_preparation'],
            description=description
        )
    print("Items created")


class Command(BaseCommand):
    help = 'Create tables'

    def handle(self, *args, **options):
        createTables()
        createCategory()
        createItemsMenu()
        print("Done")
