import pytest
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.test import Client

@pytest.fixture
def create_group():
    return Group.objects.create(name='customer')

@pytest.mark.django_db
def test_register_page_access(create_group):
    client = Client()
    response = client.get(reverse('register'))
    
    # Ensure that unauthenticated users can access the register page
    assert response.status_code == 200

    # Simulate a POST request to register a new user
    response = client.post(reverse('register'), {
        'username': 'testuser',
        'password1': 'testpassword',
        'password2': 'testpassword',
        'email': 'testuser@gmail.com'
    })

    # Ensure the user is redirected to the login page after registration
    assert response.status_code == 302
    assert response.url == reverse('login')

    # Verify that the user was created and added to the 'customer' group
    user = User.objects.get(username='testuser')
    assert user is not None
    assert user.groups.filter(name='customer').exists()