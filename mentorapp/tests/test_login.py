import pytest
from django.test import TestCase
from django.urls import reverse
from django.test import Client
from mentorapp.models import Customer, Tag, Courses, Order
from django.contrib.auth.models import User, Group

#set up to create customer and admin groups for testing
@pytest.fixture
def create_groups(db):
    Group.objects.create(name='customer')
    Group.objects.create(name='admin')





#tests the login page and returns the expected responses
@pytest.mark.django_db
def test_login_page(client):
    response = client.post('/login/', {'username' : 'testuser', 'password': 'wrongone'})
    assert response.status_code == 200
    assert b'Account does not exist.' in response.content
    
#testing the creation of a user 
# class LoginViewTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='testusers', email='testusers@gmail.com', password='testpass123')
        
#     def test_login_valid_user(self):
#         response = self.client/post('/login/', {'username' : 'testuser', 'password' : 'wrongone'})
#         self.assertRedirects(response, '/home/')
        
    # def test_login_invalid_user(self):
    #     response = self.client.post('/login/', {'username' : 'wrongusers', 'password' : 'testfail'})
    #     self.assertContains(response, 'Username or Password is incorrect or account does not exist')
    

    

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
    



@pytest.mark.django_db
def test_login_view(client):
    # Create a test user
    User.objects.create_user(username='testuser', password='testpassword123')

    # Attempt to log in with the test user credentials
    login_url = reverse('login')
    response = client.post(login_url, {'username': 'testuser', 'password': 'testpassword123'})

    # Check if the login was successful and redirected to 'home'
    assert response.status_code == 302
    assert response.url == reverse('home')

    # Check if the user is authenticated
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert response.wsgi_request.user.is_authenticated

@pytest.mark.django_db
def test_login_view_invalid_credentials(client):
    # Attempt to log in with invalid credentials
    login_url = reverse('login')
    response = client.post(login_url, {'username': 'invaliduser', 'password': 'invalidpassword'})

    # Check if the login failed and the user is redirected back to the login page
    assert response.status_code == 200
    assert 'Account does not exist.' in response.content.decode()

    # Check if the user is not authenticated
    response = client.get(reverse('home'))
    assert response.status_code == 302  # Redirect to login
    assert not response.wsgi_request.user.is_authenticated
    
    

@pytest.mark.django_db
def test_login_page(client):
    response = client.post('/login/', {'username': 'invaliduser', 'password': 'invalidpassword'})
    assert 'Account does not exist.' in response.content.decode()

@pytest.mark.django_db
def test_login_view(client):
    client.login(username='admin', password='peaches123')
    response = client.post('/login/', {'username': 'admin', 'password': 'peaches123'})
    assert response.status_code == 200
    # assert response.url == '/home/'
    

# @pytest.mark.django_db
# def test_login_invalid_user(client):
#     # Attempt to login with invalid credentials
#     response = client.post(reverse('login'), {'username': 'invaliduser', 'password': 'invalidpassword'})
    
#     # Check that the login failed and an appropriate message is displayed
#     assert response.status_code == 200
#     assert 'Username or Password is incorrect or account does not exist' in response.content.decode()
    
# @pytest.mark.django_db
# def test_logout_user(client):
#     # Create a test user and log them in
#     user = User.objects.create_user(username='testuser', password='testpassword')
#     client.login(username='testuser', password='testpassword')
    
#     # Log the user out
#     response = client.get(reverse('logout'))
    
#     # Check that the logout was successful (redirect to home page)
#     assert response.status_code == 302
#     assert response.url == reverse('home')
    

#     assert response.url == reverse('home')


@pytest.fixture
def create_user():
    user = User.objects.create_user(username='validuser', password='validpassword')
    return user

# @pytest.mark.django_db
# def test_login_valid_user(create_user):
#     client = Client()
    
#     # Test valid user login
#     response = client.post(reverse('login'), {
#         'username': 'validuser',
#         'password': 'validpassword'
#     })
    
#     # Ensure the user is redirected to the home page after login
#     assert response.status_code == 302
#     assert response.url == reverse('home')

# @pytest.mark.django_db
# def test_login_invalid_user():
#     client = Client()
    
#     # Test invalid user login
#     response = client.post(reverse('login'), {
#         'username': 'invaliduser',
#         'password': 'invalidpassword'
#     })
    
#     # Ensure the login page is reloaded with an error message
#     assert response.status_code == 200
#     assert "Account does not exist." in response.content.decode() or "Username or Password is incorrect or account does not exist" in response.content.decode()