import pytest
from pytest_bdd import scenarios, given, when, then
from django.test import Client 

scenarios('features/login.feature')

client = Client()

@given("the login page is displayed")
def login_page(db):
    response = client.get('/login/')
    assert response.status_code == 200
    
@when("the user enters valid credentials")
def valid_credentials(db):
    client.post('/login/', {'username': 'julmu', 'password': 'peaches'})
    
    
@then("the user should be redirected to the dashboard")
def dashboard(db):
    response = client.get('/dashboard/')
    assert response.status_code == 404
    
