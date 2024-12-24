import pytest
from django.contrib.auth.models import Group, User
from mentorapp.models import Customer

@pytest.fixture
def create_groups(db):
    Group.objects.create(name='admin')
    Group.objects.create(name='customer')

@pytest.fixture
def create_admin_user(db, create_groups):
    return User.objects.create_user(username='admin', password='admin')

@pytest.fixture
def create_customer(db, create_admin_user):
    return Customer.objects.create(user=create_admin_user, name='Valerie Johns', phone='01912877654', email='valeriejohns@gmail.com')

