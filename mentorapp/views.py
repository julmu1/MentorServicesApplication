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
            
            # Customer.objects.create(user=user, name=user.username, email=user.email)
            
            # Customer.objects.create(user=user, name=user.username, email=user.email)
            # username = form.cleaned_data.get('username')
            messages.success(request, f'An account was created for {{user.username}}')
            return redirect('login')
    # else:
    #     form=CreateUserForm()
        
    context = {'form': form}
    return render(request, 'mentorapp/register.html', context)





@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
# def home(request):
#     orders = Order.objects.all().order_by('id')
#     customers = Customer.objects.all()
#     # total_customers = customers.count()
#     # total_orders = orders.count()
#     pending = orders.filter(status='Pending')
#     completed = orders.filter(status='Completed')
    
#     context = {'orders': orders, 'customers' : customers,
#                'pending': pending, 
#             #    'total_orders': total_orders,
#                'completed': completed}
#     return render(request, 'mentorapp/dashboard.html', context)

def home(request):
    orders = Order.objects.select_related('customer').all()
    customers = Customer.objects.prefetch_related('order_set').all()
    # total_customers = customers.count()
    # total_orders = orders.count()
    # pending = orders.filter(status='Pending')
    # completed = orders.filter(status='Completed')
    
    context = {'orders': orders, 'customers' : customers,
               'pending': orders.filter(status='Pending'), 
               'total_orders': orders.count(),
               'completed': orders.filter(status='Completed'),
                'total_customers' : customers.count()
                }
               
    return render(request, 'mentorapp/dashboard.html', context)

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['customer'])
# def userPage(request):
#     orders = request.user.customer.order_set.all()
    
#     total_orders = orders.count()
#     pending = orders.filter(status='Pending').count()
#     completed = orders.filter(status='Completed').count()
    
#     context = {'orders' : orders, 'pending': pending, 'total_orders': total_orders,
#                'completed': completed}
#     return render(request, 'mentorapp/user.html', context)



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

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
# def customer(request, pk):
#     try:
#         customer = Customer.objects.prefetch_related('order_set').get(id=pk)
#     except Customer.DoesNotExist:
#         messages.error(request, 'Customer not found. ')
#         return redirect('home')
    
#     orders = customer.order_set.all()
#     # order_count = orders.count()
#     myFilter = OrderFilter(request.GET, queryset=orders)
#     # orders = myFilter.qs
    
#     context = {'customer': customer, 
#                'orders': myFilter.qs, 
#                'order_count': orders_count(), 
#                'myFilter': myFilter}
#     return render(request,'mentorapp/customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def profile(request):
    return render(request, 'mentorapp/customer.html')
    

@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
# def createOrder(request, pk):
#     OrderFormSet = inlineformset_factory(Customer, Order, fields=('courses', 'status'), extra=5)
#     customer = Customer.objects.get(id=pk)
#     formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
#     # form = OrderForm(initial={'customer': customer})
#     if request.method == 'POST':
#         formset = OrderFormSet(request.POST, instance=customer)
#         if formset.is_valid():
#             formset.save()
#             return redirect('customer', pk)
        
#     context={'formset': formset}
    
#     return render(request, 'mentorapp/order_form.html', context)

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

@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('home')
    
    context = {'item' : order}
    return render(request, 'mentorapp/delete_order.html', context)

# def deleteCourse(request, pk): 
#     course = Courses.objects.get(id=pk)
#     if request.method =='POST':
#         course.delete()
#         return redirect('Courses')
#     context = {'course': course }
#     return render(request, 'delete_course_confirm.html', context)

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