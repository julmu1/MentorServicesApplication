from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.signals import pre_save

class Customer(models.Model):
    user = models.OneToOneField(User,  null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name= models.CharField(max_length=60, null=True)
    
    def __str__(self):
        return self.name
 
    
class Courses(models.Model):
    
    CATEGORY = (
            ('test_based', 'test_based'),
            ('developer_based', 'developer_based'),
             ('multi-discipline', 'multi-discipline')
            )
    name = models.CharField(max_length=200, null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    difficulty = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)
    
    def __str__(self):
        return self.name
    
class Order(models.Model):
    STATUS = (
            ('Pending', 'Pending'),
            ('In Progress', 'In Progress'),
            ('Completed', 'Completed')
    )
    customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)
    courses = models.ForeignKey(Courses, null=True, on_delete= models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    
    def __str__(self):
        return f"{self.courses} order for {self.customer}."    
    