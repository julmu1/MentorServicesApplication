import pytest
from django.test import Client
from django.contrib.auth.models import User, Group
from mentorapp.models import Customer

@pytest.mark.django_db
def test_sql_injection_protection():
    # admin_group, created = Group.objects.get_or_create(name='admin')
    customer_group, created = Group.objects.get_or_create(name='customer'
                                                          )
    user = User.objects.create_user(username='sqltest', password='trerer345')
    user.groups.add(customer_group)
    
    if not Customer.objects.filter(user=user).exists():
        Customer.objects.create(user=user, name='Jane Dobbs', email='janedobbs@gmail.com')
    
    client = Client()
    malicious_input = "Jane Dobbs'; DROP TABLE mentorapp_customer; --"
    response = client.get(f'/customer/?name={malicious_input}')
    
    customer_exists = Customer.objects.filter(user=user).exists()
    assert customer_exists, "Customer data should not be deleted by SQL injection"
    assert response.status_code == 200