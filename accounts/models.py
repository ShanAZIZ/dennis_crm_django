from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    mail = models.EmailField(max_length=200, null=True)
    profile_pic = models.ImageField(default="profile1.png",null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.name)


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATS = (
        ('indoor', 'Indoor'),
        ('outdoor', 'OutDoor'),
    )
    name = models.CharField(max_length=200)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATS)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATS = (
        ('pending', 'Pending'),
        ('Out of Delivery', 'Out of Delivery'),
        ('Delivered', 'Delivered'),
    )
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATS)
    note = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.product.name


