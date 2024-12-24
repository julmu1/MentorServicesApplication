import pytest
from django.contrib.auth.models import User, AnonymousUser
from django.test import RequestFactory
from django.http import HttpResponse
from django.urls import reverse
from mentorapp.decorators import unauthenticated_user, allowed_users, admin_only
from mentorapp.views import loginPage, registerPage, courses

@pytest.mark.django_db
def test_admin_only_allows_access():
    user = User.objects.create_user(username='testadminuser', password='testadmin123')
    group = Group.objects.create(name='admin')
    user.groups.add(group)
    
    factory = RequestFactory()
    request = factory.get(revers('courses'))
    request.user = user
    
    response = courses(request)
    assert response.status_code == 200
    assert "mentorapp/courses.html" in response.template_name