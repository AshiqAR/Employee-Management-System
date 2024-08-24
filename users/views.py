from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import HttpResponse

def is_in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

# Create your views here.
def index(request):
    return render(request, 'users/index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        authenticated_user = authenticate(username=username, password=password)
        if authenticated_user is not None and authenticated_user.is_active and not authenticated_user.is_superuser:
            login(request, authenticated_user)
            if role == 'admin' and is_in_group(authenticated_user, 'hr'):
                return redirect('admin_dashboard:index')
            elif role == 'employee' and is_in_group(authenticated_user, 'employees'):
                return redirect('employees:index')
            else:
                messages.error(request, "Invalid Credentials.")
                return redirect('users:login')
        else:
            messages.error(request, "Invalid Credentials.")
            return redirect('users:login')

    return render(request, 'users/login.html')
