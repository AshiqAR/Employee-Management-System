from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.models import User
from .models import Employee

def group_required(group_name):
    def in_group(user):
        return user.is_authenticated and user.groups.filter(name=group_name).exists()
    return user_passes_test(in_group)

def validate_password(password):
    if len(password) < 8:
        return False, 'Password must be at least 8 characters long.'
    if not any(char.isdigit() for char in password):
        return False, 'Password must contain at least one digit.'
    if not any(char.isupper() for char in password):
        return False, 'Password must contain at least one uppercase letter.'
    if not any(char.islower() for char in password):
        return False, 'Password must contain at least one lowercase letter.'
    return True, None

@group_required('employee')
def index(request):
    user = get_object_or_404(User, username=request.user.username)
    employee = get_object_or_404(Employee, user_account=user)
    if user.check_password(f'{employee.first_name.capitalize()}@{employee.employee_id}'):
        return redirect('employees:change_password')
    return render(request, 'employees/index.html')

@group_required('employee')
def change_password(request):
    user = get_object_or_404(User, username=request.user.username)
    employee = get_object_or_404(Employee, user_account=user)
    context = {'employee': employee}
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if not user.check_password(current_password):
            context['error'] = 'Incorrect current password.'
        elif user.check_password(new_password):
            context['error'] = 'New password cannot be the same as the current password.'
        elif new_password != confirm_password:
            context['error'] = 'Passwords do not match.'
        else:
            valid, error = validate_password(new_password)
            if valid:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                return redirect('employees:index')
            context['error'] = error
    return render(request, 'employees/change_password.html', context)

@group_required('employee')
def my_account_view(request):
    user = get_object_or_404(User, username=request.user.username)
    employee = get_object_or_404(Employee, user_account=user)
    return render(request, 'employees/account.html', {'employee': employee})

@group_required('employee')
def notifications_view(request):
    return render(request, 'employees/notifications.html')

@group_required('employee')
def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('users:login')