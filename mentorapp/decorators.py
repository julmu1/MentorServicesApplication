from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect ('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

#method which sets groups as allowed users to restrict views
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
        
            # if request.user.groups.exists():
            g = request.user.groups.values_list('name', flat=True)
            groups = list(g)
            
            if set(groups) & set(allowed_roles):
                return view_func(request, *args, **kwargs)
            else:
                
                
            # if group in allowed_roles:
            #     return view_func(request, *args, **kwargs)
            # else:
            #when a user reaches a restricted view they encounter a descriptive message and a link to return to the dashboard
                return HttpResponse(
                    "<h2>At this time you are not authorised to view this page, as it is restricted. Please reach out to the People services manager for more information</h2>"
                    f"<p><a href='{reverse('home')}' >Return to the Dashboard</a></p>")
        return wrapper_func
    return decorator

#method to ensure only admin have access to certain functionality
def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'customers':
            return redirect('user-page')
        
        if group == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')
        
    return wrapper_function