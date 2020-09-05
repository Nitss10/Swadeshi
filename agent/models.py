from django.db import models

class Agent(models.Model):
    name = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100) 
    mobile = models.CharField(max_length=12) 
    pincode = models.CharField(max_length = 6) 
    address = models.CharField(max_length = 300)
    aadhar = models.CharField(max_length = 12) 
    image = models.ImageField(upload_to='agent-image/', blank=True, default = "")

    def __str__(self): 
        return self.name

class Manufacturer(models.Model):
    agent_id = models.ForeignKey('Agent', on_delete=models.CASCADE)
    name = models.CharField(max_length = 100)
    company_name = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100, blank=True) 
    mobile = models.CharField(max_length=12) 
    pincode = models.CharField(max_length = 6) 
    address = models.CharField(max_length = 300)
    aadhar = models.CharField(max_length = 12) 
    image = models.ImageField(upload_to='agent-image/', blank=True, default = "")

    def __str__(self): 
        return self.company_name


class Product(models.Model):
    manufacturer_id = models.ForeignKey('Manufacturer', on_delete=models.CASCADE)
    name = models.CharField(max_length = 50)
    category = models.ForeignKey('Category', on_delete=models.SET_DEFAULT, default = "other") 
    quantity = models.IntegerField(default = 1)
    description = models.CharField(max_length = 300)
    price = models.IntegerField()
    image = models.ImageField(upload_to='prod-image/', default = "")

    def __str__(self): 
        return self.name

class Category(models.Model):
    name = models.CharField(max_length = 50)

    def __str__(self): 
        return self.name
