import pytest
from django.test import Client, TestCase
from mentorapp.models import Customer, Tag, Courses, Order
from django.contrib.auth.models import User, Group


@pytest.fixture
def create_admin_user(db):
    return User.objects.create_superuser(username='admin', password='admin', email='admin@example.com')

@pytest.fixture
def create_customer(db, create_admin_user):
    return Customer.objects.create(user=create_admin_user, name='Valerie Johns', phone='01912877654', email='valeriejohns@gmail.com')

# @pytest.mark.django_db
# def test_customer_creation(create_customer):
#     customer = create_customer
#     assert customer.name == 'Valerie Johns'
#     assert customer.phone == '01912877654'
#     assert customer.email == 'valeriejohns@gmail.com'
#     assert str(customer) == 'Valerie Johns'

@pytest.fixture
def create_admin_user(db):
    return User.objects.create_superuser(username='julmu', password='peaches', email='julmu@gmail.com')

@pytest.fixture
def create_customer(db, create_admin_user):
    return Customer.objects.create(user=create_admin_user, name='Valerie Johns', phone='01912877654', email='valeriejohns@gmail.com')

# @pytest.mark.django_db
# def test_customer_creation(create_admin_user, create_customer):
#     customer = create_customer
#     assert customer.name == 'Valerie Johns'
#     assert customer.phone == '01912877654'
#     assert customer.email == 'valeriejohns@gmail.com'
#     assert str(customer) == 'Valerie Johns'

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

# @pytest.mark.django_db
# def test_customer_creation(create_admin_user, create_customer, create):
#     customer = create_customer
#     assert customer.name == 'Valerie Johns'
#     assert customer.phone == '01912877654'
#     assert customer.email == 'valeriejohns@gmail.com'
#     assert str(customer) == 'Valerie Johns'
    
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
    
    
    
# @pytest.mark.django_db
# def test_order_creation(create_customer, create_order):
#     order = Order.objects.create(
#         customer=create_customer,
#         courses=create_course,
#         status='Pending'
#     )
#     assert order.customer.user.groups.filter(name='Admin').exists()
#     assert order.status == 'Pending'
#     assert order.customer.name =='Valerie Johns'
#     assert order.courses.name == 'Django Basics'
#     assert order.status == 'Pending'
#     assert str(order) == f"A Django Users course order for Valerie Johns. "
    

class CustomerTestCase(TestCase):
    def setUp(self):
        Customer.objects.create(name="John Doe", email="john@example.com")
        Customer.objects.create(name="Jane Doe", email="jane@example.com")

    def test_customer_email(self):
        john = Customer.objects.get(name="John Doe")
        self.assertEqual(john.email, "john@example.com")
    

class CustomerModelTest(TestCase):
    def setUp(self):
        user = User.objects.create(username="john_doe", password="password")
        self.customer = Customer.objects.create(user=user, name="John Doe", phone="1234567890", email="john@example.com")

    # def test_customer_str(self):
    #     self.assertEqual(str(self.customer), self.customer.name)

class TagModelTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="Test Tag")

    def test_tag_str(self):
        self.assertEqual(str(self.tag), self.tag.name)

class CoursesModelTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="Test Tag")
        self.course = Courses.objects.create(name="Test Course", category="test_based", difficulty="Easy")

    def test_courses_str(self):
        self.assertEqual(str(self.course), self.course.name)

class OrderModelTest(TestCase):
    def setUp(self):
        user = User.objects.create(username="john_doe", password="password")
        customer = Customer.objects.create(user=user, name="John Doe", phone="1234567890", email="john@example.com")
        course = Courses.objects.create(name="Test Course", category="test_based", difficulty="Easy")
        self.order = Order.objects.create(customer=customer, courses=course, status="Pending")

    # def test_order_str(self):
    #     self.assertEqual(str(self.order), f"{self.order.courses} order for {self.order.customer}.")
        



class OrderModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="john_doe", password="password")
        customer = Customer.objects.create(user=user, name="John Doe", phone="1234567890", email="john@example.com")
        course = Courses.objects.create(name="Test Course", category="test_based", difficulty="Easy")
        self.order = Order.objects.create(customer=customer, courses=course, status="Pending")

    # def test_order_str(self):
    #     self.assertEqual(str(self.order), f"{self.order.courses} order for {self.order.customer}.")
        
        
        
