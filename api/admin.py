from django.contrib import admin
from .models import Product, Location, Transfer, HistoryOfTransfer, HistoryOfLoginToZakuro

admin.site.register(Product)
admin.site.register(Location)
admin.site.register(Transfer)
admin.site.register(HistoryOfTransfer)

admin.site.register(HistoryOfLoginToZakuro)

