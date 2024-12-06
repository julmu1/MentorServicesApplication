import pytest
from django.test import Client
from mentorapp.models import Customer, Tag, Courses, Order
from django.contrib.auth.models import User, Group

@pytest.mark.django_db
def test_order_creation():
    customer = Customer.objects.create(name='julmu', email='julmu@gmail.com')
    course = Courses.objects.create(name='ISTQB', category='')
    
@pytest.fixture
def create_admin_user(db):
    group, _ = Group.objects.get_or_create(name='admin')
    user = User.objects.create_user(username='adminuser', password='authorised123')
    user.groups.add(group)
    return user

@pytest.fixture
def create_customer_user(db):
    group, _ = Group.objects.get_or_create(name='customer')
    user = User.objects.create_user(username='customeruser', password='authorised123')
    user.groups.add(group)
    return user

    # return User.objects.create_user(username='testuser', password='Applepie123')

@pytest.fixture
def client_logged_in_admin(create_admin_user):
    client = Client()
    client.login(username='adminuser', password='authorised123')
    return client

@pytest.fixture
def client_logged_in_customer(create_customer_user):
    client = Client()
    client.login(username='customeruser', password='authorised123')
    return client

@pytest.fixture
def create_tag(db):
    return Tag.objects.create(name='Python')

@pytest.fixture
def create_course(db, create_tag):
    course = Courses.objects.create(
        name = 'Django Basics',
        category = 'developer_based',
        difficulty='Intermediate',
        description= 'A beginner level course for first time Django Users'
    )
    course.tags.add(create_tag)
    return course

@pytest.mark.django_db
def test_customer_creation(create_admin_user, create_customer, create):
    customer = create_customer
    assert customer.name == 'Valerie Johns'
    assert customer.phone == '01912877654'
    assert customer.email == 'valeriejohns@gmail.com'
    assert str(customer) == 'Valerie Johns'
    
@pytest.mark.django_db
def test_tag_creation(create_tag):
    tag = create_tag
    assert tag.name == 'Python'
    assert str(tag) == 'Python'
    
@pytest.mark.django_db
def test_course_creation(create_course):
    course = create_course
    assert course.name == 'Django Basics'
    assert course.category == 'developer_based'
    assert course.difficulty == 'Intermediate'
    assert course.description == 'A beginner level course for first time Django Users'
    assert str(course) == 'Django Basics'
    assert course.tags.count() == 1
    
@pytest.mark.django_db
def test_order_creation(create_customer, create_order):
    order = Order.objects.create(
        customer=create_customer,
        courses=create_course,
        status='Pending'
    )
    assert order.customer.user.groups.filter(name='Admin').exists()
    assert order.status == 'Pending'
    # assert order.customer.name =='Valerie Johns'
    # assert order.courses.name == 'Django Basics'
    # assert order.status == 'Pending'
    # assert str(order) == f"A Django Users course order for Valerie Johns. "
    