from django.contrib import admin
from .models import Product, Location, Transfer, HistoryOfTransfer, HistoryOfLoginToZakuro, Car, Rental

admin.site.register(Product)
admin.site.register(Location)
admin.site.register(Transfer)
admin.site.register(HistoryOfTransfer)

admin.site.register(HistoryOfLoginToZakuro)

admin.site.register(Car)
admin.site.register(Rental)