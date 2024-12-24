import pytest
from django.test import Client
from django.contrib.auth.models import User, Group
from mentorapp.models import Customer

@pytest.mark.django_db
def test_sql_injection_protection(client):
    response = client.get('/path/to/view/?param=1\' OR \'1\'=\'1')
    assert response.status_code == 404  
    
    #this test will assess the protection of the application from sql injection