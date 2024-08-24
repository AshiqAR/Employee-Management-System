from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test

def group_required(group_name):
    def in_group(user):
        return user.groups.filter(name=group_name).exists()
    return user_passes_test(in_group)

@group_required('hr')
def index(request):
    return render(request, 'admin_dashboard/dashboard.html')

@group_required('hr')
def add_employee(request):
    return render(request, 'admin_dashboard/add_employee.html')

@group_required('hr')
def view_employees(request):
    return render(request, 'admin_dashboard/view_employees.html')

@group_required('hr')
def add_attendance(request):
    return render(request, 'admin_dashboard/add_attendance.html')

@group_required('hr')
def leave_requests(request):
    return render(request, 'admin_dashboard/leave_requests.html')

@group_required('hr')
def notifications(request):
    return HttpResponse("Hello, world. You're at the notifications page.")

@group_required('hr')
def logout_view(request):
    return HttpResponse("Hello, world. You're at the logout page.")