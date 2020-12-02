from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Product(models.Model):
    index = models.IntegerField(validators=[MinValueValidator(100), MaxValueValidator(999)], unique=True)
    name = models.CharField(max_length=64)
    ean = models.BigIntegerField(unique=True,)

class Location(models.Model):
    location = models.CharField(max_length=20, unique=True)

class Transfer (models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    pcs = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_transfer = models.DateField(auto_now=True)

    def location_name(self):
        return self.location.location

    def product_name(self):
        return self.product.name

    def product_index(self):
        return self.product.index

    def user_name(self):
        return self.user.username;

    class Meta:
        unique_together = (('product', 'location'),)
        index_together = (('product', 'location'),)

class HistoryOfTransfer (models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    locationFrom = models.ForeignKey(Location, related_name="fromLocation", on_delete=models.CASCADE)
    locationTo = models.ForeignKey(Location, related_name="toLocation", on_delete=models.CASCADE)
    pcs = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_transfer = models.DateField(auto_now=True)

    def location_name_from(self):
        return self.locationFrom.location

    def location_name_to(self):
        return self.locationTo.location

    def product_name(self):
        return self.product.name

    def product_index(self):
        return self.product.index

    def user_name(self):
        return self.user.username;
# //////////////////FOR ZAKURO//////////////////////////////////////////////////////////////////
class HistoryOfLoginToZakuro (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timeAndDate = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user.username
# //////////////////FOR RENTAL/////////////////////////////////////////////////////
class Car (models.Model):
    car = models.CharField(max_length=64)
    carPicture = models.CharField(max_length=64)
    seats = models.IntegerField()
    trunk = models.CharField(max_length=64)
    price = models.IntegerField()
    fuel = models.CharField(max_length=64, default='benzyna')
    gearbox = models.CharField(max_length=64, default='manualna')

class Rental (models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rentFrom = models.DateTimeField()
    rentTo = models.DateTimeField()
    firstName = models.CharField(max_length=64)
    lastName = models.CharField(max_length=64)
    phoneNumber = models.BigIntegerField()
    email = models.CharField(max_length=64)
