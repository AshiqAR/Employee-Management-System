from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from django.http import HttpResponse

from django.contrib.auth.decorators import user_passes_test
from employees.models import Designation, Employee, Document, EmployeeUpdate
from attendance.models import Attendance
from leave.models import Leave, LeaveRequest

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
    return HttpResponse("Hello, world. You're at the notifications page.")

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
def my_account(request):
    return HttpResponse("You're at the My Account page.")

@group_required('hr')
def employee_update_requests(request):
    update_requests = EmployeeUpdate.objects.all()
    return render(request, 'admin_dashboard/employee_update_requests.html', {'update_requests': update_requests})