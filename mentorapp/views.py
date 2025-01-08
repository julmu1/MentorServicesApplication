from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm, CoursesForm
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, admin_only

@unauthenticated_user
def loginPage(request):    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        elif not User.objects.filter(username=username).exists():
            messages.error(request, 'Account does not exist.')
        else:
            messages.error(request, 'Username or Password is incorrect or account does not exist')
    context = {}
    return render(request, 'mentorapp/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

@unauthenticated_user
def registerPage(request):    
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            #adding new lines for linking new user to customer group and instance
            if not Customer.objects.filter(user=user).exists():
                Customer.objects.create(
                    user=user,
                    name=user.username,
                    email=user.email
                )
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            messages.success(request, f'An account was created for {{user.username}}')
            return redirect('login')
        
    context = {'form': form}
    return render(request, 'mentorapp/register.html', context)


# this is the current home method after some reworking
@login_required(login_url='login')
def home(request):
    orders = Order.objects.select_related('customer').all()
    customers = Customer.objects.prefetch_related('order_set').all()
    
    context = {'orders': orders, 'customers' : customers,
               'pending': orders.filter(status='Pending'), 
               'total_orders': orders.count(),
               'completed': orders.filter(status='Completed'),
                'total_customers' : customers.count()
                }
               
    return render(request, 'mentorapp/dashboard.html', context)

@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    
    orders = customer.order_set.all()
    order_count = orders.count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    
    context = {'customer': customer, 'orders': orders, 
            #    'order_count': order_count, 
               'myFilter': myFilter}
    return render(request,'mentorapp/customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def profile(request):
    return render(request, 'mentorapp/customer.html')
    
def createOrder(request, pk):
    customer = Customer.objects.get(id=pk)
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form' : form}
    
    return render(request, 'mentorapp/order_form.html', context)



@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form': form}

    return render(request, 'mentorapp/order_form.html', context)

#adding method to ensure only admin can delete an order and an error is triggered if a regular user tries
@login_required(login_url='login')
def deleteOrder(request, pk):
    # Fetch the order by primary key
    order = Order.objects.get(id=pk)
    
    # Check if the logged-in user is an admin
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to delete this order.")

        # If the user is not an admin, redirect or show a permission error
        return redirect('home')  # Redirect to home page or show a 'permission denied' message
    
    if request.method == "POST":
        # Delete the order
        order.delete()
        messages.success(request, "Order deleted successfully.")

        return redirect('home')
    
    # Render confirmation page
    context = {'item': order}
    return render(request, 'mentorapp/delete_order.html', context)



# @login_required(login_url='login')
# # @allowed_users(allowed_roles=['admin'])
# def deleteOrder(request, pk):
#     order = Order.objects.get(id=pk)
#     if request.method == "POST":
#         order.delete()
#         return redirect('home')
    
#     context = {'item' : order}
#     return render(request, 'mentorapp/delete_order.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def mentorappSettings(request):
    customer = request.user.customer
    form =  CustomerForm(instance=customer)
    context = {'form' : form}
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES,instance=customer)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    return render(request, 'mentorapp/mentorapp_settings.html', context)

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def courses(request):
    courses = Courses.objects.all()
    return render(request,'mentorapp/courses.html', {'courses': courses})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_courses(request):
    form = CoursesForm()
    context = {'form' : form}
    
    if request.method == 'POST':
        form = CoursesForm(request.POST)
        if form.is_valid():
            #courses were not being saved as form.save did not have closing parentheses
            form.save()
            return redirect ('courses')
    return render(request, 'mentorapp/create_courses.html', context)

#A method to delete a course which currently has errors and needs debugging 
# def deleteCourse(request, pk): 
#     course = Courses.objects.get(id=pk)
#     if request.method =='POST':
#         course.delete()
#         return redirect('Courses')
#     context = {'course': course }
#     return render(request, 'delete_course_confirm.html', context)

