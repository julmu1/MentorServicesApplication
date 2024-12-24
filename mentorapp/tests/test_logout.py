import pytest
from django.urls import reverse
from django.test import Client
from mentorapp.models import Customer, Tag, Courses, Order
from django.contrib.auth.models import User, Group

@pytest.mark.django_db
def test_logout_user(client_logged_in_as_admin):
    response = client_logged_in_admin.get(reverse('/logout/'))
    assert response.status_code == 302
    


@pytest.fixture
def create_user():
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user

@pytest.mark.django_db
def test_logout_user(create_user):
    client = Client()

    # Log in the user first
    client.login(username='testuser', password='testpassword')
    
    # Test user logout
    response = client.get(reverse('logout'))
    
    # Ensure the user is redirected to the home page after logout
    assert response.status_code == 302
    assert response.url == reverse('home')

    # Verify that the user is logged out
    response = client.get(reverse('home'))
    assert response.wsgi_request.user.is_anonymous