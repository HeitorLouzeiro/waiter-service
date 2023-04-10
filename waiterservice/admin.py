from django.contrib import admin

# Register your models here.
from .models import Category, Commands, ItemMenu, ItemPedido, Table


class CommandsAdmin(admin.ModelAdmin):
    list_display = ('code', 'Table', 'opening', 'closed', 'status', 'amount')
    list_filter = ('status', 'Table')
    search_fields = ('Table__number',)


admin.site.register(Table)
admin.site.register(Commands, CommandsAdmin)
admin.site.register(Category)
admin.site.register(ItemMenu)
admin.site.register(ItemPedido)
