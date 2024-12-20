from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import Customer, Courses

def customer_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)
        
        Customer.objects.create(
            user=instance,
            name=instance.username,
            )
       
def courses_create(sender, instance, created, **kwarfs):
    if created:
        print('signal is received')
        
post_save.connect(customer_profile, sender=User)
post_save.connect(courses_create, sender=Courses)