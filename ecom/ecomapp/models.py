from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.
class filtering(models.Manager): # this is a Custom Manager
    def mobile(self):
        return self.filter(category__iexact = 'Mobile')
    def laptop(self):
        return self.filter(category__iexact = 'Laptop')
    def tv(self):
        return self.filter(category__iexact = 'TV')
    

class Product(models.Model):
    pid=models.IntegerField(primary_key=True)
    pname=models.CharField(max_length=255)
    type=[('Mobile','Mobile'),('Laptop','Laptop'),('TV','TV')]
    category= models.CharField(max_length=255,choices=type)
    desc =models.CharField(max_length=255)
    price=models.IntegerField()
    image=models.ImageField(upload_to='media')
    objects = models.Manager()
    filter=filtering()

class Cart(models.Model):
    pid=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    date_added=models.DateField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,default="", blank=True, null=True)

class Order(models.Model):
    oid=models.CharField(max_length=50,default=0)
    pid=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    date_added=models.DateField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,default="", blank=True, null=True)
    is_completed=models.BooleanField(default=False)

class Address(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    address=models.CharField(max_length=255)
    zip=models.PositiveIntegerField(validators=[MaxValueValidator(999999),MinValueValidator(100000)])
    phone=models.BigIntegerField()

    def __str__(self):
        return self.address