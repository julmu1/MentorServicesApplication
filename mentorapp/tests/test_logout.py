import pytest
from django.urls import reverse
from django.test import Client
from mentorapp.models import Customer, Tag, Courses, Order
from django.contrib.auth.models import User, Group

@pytest.mark.django_db
def test_logout_user(client_logged_in_admin):
    response = client_logged_in_admin.get(reverse('/logout/'))
    assert response.status_code == 302