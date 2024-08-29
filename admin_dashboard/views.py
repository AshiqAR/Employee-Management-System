from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout, update_session_auth_hash
from django.http import HttpResponse
from django.contrib import messages

from employees.models import Designation, Employee, Document, EmployeeUpdate
from attendance.models import Attendance
from leave.models import Leave, LeaveRequest
from django.contrib.auth.models import User

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

def group_required(group_name):
    def in_group(user):
        return user.groups.filter(name=group_name).exists()
    return user_passes_test(in_group)

@group_required('hr')
def add_employee(request):
    designations = Designation.objects.all()
    return render(request, 'admin_dashboard/add_employee.html', {'designations': designations})

@group_required('hr')
def index(request):
    employees = Employee.objects.all()
    designations = Designation.objects.all()
    return render(request, 'admin_dashboard/view_employees.html', {'employees': employees, 'designations': designations})

@group_required('hr')
def add_attendance(request):
    employees = Employee.objects.all()
    return render(request, 'admin_dashboard/add_attendance.html', {'employees': employees})

@group_required('hr')
def leave_requests(request):
    leaves = Leave.objects.all()
    leave_requests = LeaveRequest.objects.all()
    return render(request, 'admin_dashboard/leave_requests.html', {'leaves': leaves, 'leave_requests': leave_requests})

@group_required('hr')
def review_leave_request(request, leave_request_id):
    leave_request = get_object_or_404(LeaveRequest, leave_request_id=leave_request_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            leave_request.status = 'approved'
            leave_request.start_date = request.POST.get('approval_start_date')
            leave_request.end_date = request.POST.get('approval_end_date')
            leave_request.comments = request.POST.get('comments')

            print('start date:', leave_request.start_date)
            print('approved')

        elif action == 'reject':
            leave_request.status = 'rejected'
            leave_request.comments = request.POST.get('comments')
            print('rejected')
            
        return redirect('admin_dashboard:review_leave_request', leave_request_id=leave_request_id)
    
    # Render the form for GET requests or after POST processing
    return render(request, 'admin_dashboard/review_leave_request.html', {'leave_request': leave_request})


@group_required('hr')
def notifications(request):
    return render(request, 'admin_dashboard/notifications.html')

@group_required('hr')
def logout_view(request):
    logout(request)
    return redirect('users:login')

@group_required('hr')
def edit_employee(request, employee_id):
    employee = Employee.objects.get(employee_id=employee_id)
    designations = Designation.objects.all()
    return render(request, 'admin_dashboard/edit_employee.html', {'employee': employee, 'designations': designations})

@group_required('hr')
def employee_details(request, employee_id):
    employee = get_object_or_404(Employee, employee_id=employee_id)
    
    # Retrieve today's attendance
    today = timezone.now().date()
    attendance = Attendance.objects.filter(employee_id=employee.employee_id, date=today).first()
    
    # Retrieve employee documents
    documents = Document.objects.filter(employee_id=employee.employee_id)
    
    context = {
        'employee': employee,
        'attendance': attendance,
        'documents': documents,
    }
    
    return render(request, 'admin_dashboard/employee_details.html', context)

@group_required('hr')
def my_account_view(request):
    user = get_object_or_404(User, id=request.user.id)
    employee = get_object_or_404(Employee, user_account=user)

    context = {
        'user': user,
        'employee': employee,
    }

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'change_username':
            new_username = request.POST.get('new_username')
            if User.objects.filter(username=new_username).exists():
                context['username_error'] = 'Username already exists.'
            else:
                user.username = new_username
                user.save()
                messages.success(request, 'Username changed successfully.')
                return redirect('admin_dashboard:my_account')

        elif action == 'change_password':
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            is_valid, error = validate_password(new_password)

            if not user.check_password(current_password):
                context['password_error'] = 'Current password is incorrect.'
            elif new_password != confirm_password:
                context['password_mismatch'] = 'Passwords do not match.'
            elif not is_valid: 
                context['password_error'] = error
            else:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password changed successfully.')
                return redirect('admin_dashboard:my_account')

    return render(request, 'admin_dashboard/my_account.html', context)


@group_required('hr')
def employee_update_requests(request):
    update_requests = EmployeeUpdate.objects.all()
    return render(request, 'admin_dashboard/employee_update_requests.html', {'update_requests': update_requests})