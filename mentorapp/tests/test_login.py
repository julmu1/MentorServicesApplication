import pytest
from django.test import TestCase
from django.urls import reverse
from django.test import Client
from mentorapp.models import Customer, Tag, Courses, Order
from django.contrib.auth.models import User, Group

@pytest.fixture
def create_groups(db):
    Group.objects.create(name='customer')
    Group.objects.create(name='admin')

@pytest.mark.django_db
def test_login_page(client):
    response = client.post('/login/', {'username' : 'testuser', 'password': 'wrongone'})
    assert response.status_code == 200
    assert b'Username or Password is incorrect or account does not exist' in response.content
    
class LoginViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testusers', password='testpass123')
        
    def test_login_valid_user(self):
        response = self.client/post('/login/', {'username' : 'testusers', 'password' : 'testpass'})
        self.assertRedirects(response, '/home/')
        
    def test_login_invalid_user(self):
        response = self.client.post('/login/', {'username' : 'wrongusers', 'password' : 'testpass'})
        self.assertContains(response, 'Username or Password is incorrect')
    

    

    # group = Group.objects.create(name='Mentor')
    
    # user = User.objects.create_user(username="TestUser", email="TestUser@gmail.com", password="Applepie123")
    # # user.groups.add(group)
    
    # response = client.post(reverse('login'), {'username' : 'Testuser', 'email' : 'TestUser@gmail.com','password': 'Applepie123'})
    
    # assert response.status_code == 302
    # assert response.url == ('home')
    
@pytest.mark.django_db
def test_register_page(client, create_groups):
    response = client.post('/register/', {'username' : 'newuser', 'password1': 'Applepie123', 'password2' : 'Applepie123'})
    assert response.status_code == 302
    