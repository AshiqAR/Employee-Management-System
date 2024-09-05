from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout, update_session_auth_hash
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.db import IntegrityError

from employees.models import Designation, Employee, Document, EmployeeUpdate, Department
from attendance.models import Attendance
from leave.models import Leave, LeaveRequest, LeaveStatus
from datetime import date

from django.contrib.auth.models import User, Group

from .forms import EmployeeForm, AttendanceForm

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

def clear_messages(request):
    storage = messages.get_messages(request)
    for message in storage:
        pass

def group_required(group_name):
    def in_group(user):
        return user.is_authenticated and user.groups.filter(name=group_name).exists()
    return user_passes_test(in_group)

@group_required('hr')
def add_employee(request):
    form = EmployeeForm()
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            try:
                user_account = User.objects.create_user(
                    username=form.cleaned_data['email'],
                    email=form.cleaned_data['email'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    password=f"{form.cleaned_data['first_name'].lower()}@123",
                    is_staff=True if form.cleaned_data['role'] == 'hr' else False
                )
                group = Group.objects.get(name=form.cleaned_data['role'])
                user_account.groups.add(group)
            except Exception as e:
                messages.error(request, "A user with the same username or email already exists.")
                return redirect('admin_dashboard:add_employee')

            form.save(user_account=user_account)
            messages.success(request, 'Employee added successfully.')
            return redirect('admin_dashboard:index')
    return render(request, 'admin_dashboard/add_employee.html', {'form': form})

@group_required('hr')
def index(request):
    employees = Employee.objects.all()
    designations = Designation.objects.all()
    return render(request, 'admin_dashboard/view_employees.html', {'employees': employees, 'designations': designations})

@group_required('hr')
def add_attendance(request):
    today = date.today()
    employees = Employee.objects.all()

    if request.method == 'POST':
        attendance_date = request.POST.get('attendance_date')
        for employee in employees:
            form = AttendanceForm(request.POST, prefix=str(employee.employee_id))
            if form.is_valid():
                attendance = form.save(commit=False)
                attendance.employee = employee
                attendance.date = attendance_date
                attendance.save()
        return redirect('attendance:add_attendance')

    employee_forms = [(employee, AttendanceForm(prefix=str(employee.employee_id))) for employee in employees]

    context = {
        'today': today,
        'employee_forms': employee_forms,
    }
    return render(request, 'admin_dashboard/add_attendance.html', context)

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
        comments = request.POST.get('comments')
        approval_start_date = request.POST.get('approval_start_date')
        approval_end_date = request.POST.get('approval_end_date')

        if action == 'approve':
            # Validate approval dates
            if not approval_start_date or not approval_end_date:
                return render(request, 'admin_dashboard/review_leave_request.html', {
                    'leave_request': leave_request,
                    'error': 'Approval dates are required'
                })
            
            if approval_start_date > approval_end_date:
                return render(request, 'admin_dashboard/review_leave_request.html', {
                    'leave_request': leave_request,
                    'error': 'Approval end date cannot be before start date'
                })

            # Approve the leave
            leave_request.remarks = comments
            leave_request.approve_leave(approval_start_date, approval_end_date)
            print('Leave request approved')

        elif action == 'reject':
            leave_request.remarks = comments
            leave_request.reject_leave()
            print('Leave request rejected')
        
        return redirect('admin_dashboard:leave_requests')
    
    return render(request, 'admin_dashboard/review_leave_request.html', {
        'leave_request': leave_request
    })


@group_required('hr')
def notifications(request):
    return render(request, 'admin_dashboard/notifications.html')

@group_required('hr')
def logout_view(request):
    logout(request)
    return redirect('users:login')

@group_required('hr')
def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, employee_id=employee_id)
    clear_messages(request)
    if request.method == 'POST':
        employee.email = request.POST.get('email', employee.email)
        employee.phone_number = request.POST.get('phone_number', employee.phone_number)
        employee.date_of_joining = request.POST.get('date_of_joining', employee.date_of_joining)
        employee.address = request.POST.get('address', employee.address)
        employee.experience_description = request.POST.get('experience_description', employee.experience_description)

        department_id = request.POST.get('department', employee.department_id)
        if department_id:
            employee.department = get_object_or_404(Department, department_id=department_id)

        designation_id = request.POST.get('designation', employee.designation_id)
        if designation_id:
            employee.designation = get_object_or_404(Designation, designation_id=designation_id)

        supervisor_id = request.POST.get('supervisor_employee_id', employee.supervisor.employee_id if employee.supervisor else None)
        if supervisor_id:
            if int(supervisor_id) == employee_id:
                messages.error(request, 'Employee cannot be their own supervisor.')
                return redirect('admin_dashboard:edit_employee', employee_id=employee_id)
            employee.supervisor = get_object_or_404(Employee, employee_id=supervisor_id)
        else:
            employee.supervisor = None  # Handle the case when no supervisor is selected

        employee.save()

        messages.success(request, 'Employee details updated successfully.')
        return redirect('admin_dashboard:edit_employee', employee_id=employee_id)

    departments = Department.objects.all()
    designations = Designation.objects.all()
    documents = Document.objects.filter(employee_id=employee_id)
    context = {
        'employee': employee,
        'departments': departments,
        'designations': designations,
        'documents': documents,
    }
    
    return render(request, 'admin_dashboard/edit_employee.html', context)

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
    documents = Document.objects.filter(validated=False)
    return render(request, 'admin_dashboard/employee_update_requests.html', {'update_requests': update_requests, 'documents': documents})

@group_required('hr')
def handle_document_validation(request, document_id):
    document = get_object_or_404(Document, document_id=document_id)
    action = request.POST.get('action')

    if action == 'approve':
        document.validated = True
        document.save()
        messages.success(request, 'Document approved.')
    elif action == 'reject':
        document.delete()
        messages.success(request, 'Document rejected.')

    return redirect('admin_dashboard:employee_update_requests')

@group_required('hr')
def handle_employee_update_request(request, request_id):
    update_request = get_object_or_404(EmployeeUpdate, request_id=request_id)
    employee = update_request.employee_id

    # Determine if the request is to approve or reject
    action = request.POST.get('action')

    if action == 'approve':
        # Apply the requested changes to the employee profile
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        emergency_contact_name = request.POST.get('emergency_contact_name')
        emergency_contact_number = request.POST.get('emergency_contact_number')
        emergency_contact_relationship = request.POST.get('emergency_contact_relationship')
        experience_description = request.POST.get('experience_description')
        bank_name = request.POST.get('bank_name')
        bank_account_number = request.POST.get('bank_account_number')
        ifsc_code = request.POST.get('ifsc_code')
        bank_branch = request.POST.get('bank_branch')

        if update_request.profile_edit:
            employee.email = email or update_request.email or employee.email
            employee.phone_number =  phone_number or update_request.phone_number or employee.phone_number
            employee.address = address or update_request.address or employee.address
            employee.emergency_contact_name = emergency_contact_name or update_request.emergency_contact_name or employee.emergency_contact_name
            employee.emergency_contact_number = emergency_contact_number or update_request.emergency_contact_number or employee.emergency_contact_number
            employee.emergency_contact_relationship = emergency_contact_relationship or update_request.emergency_contact_relationship or employee.emergency_contact_relationship
            employee.experience_description = experience_description or update_request.experience_description or employee.experience_description
            employee.has_profile_edit = False

        if update_request.bank_edit:
            employee.bank_name = bank_name or update_request.bank_name or employee.bank_name
            employee.bank_account_number = bank_account_number or update_request.bank_account_number or employee.bank_account_number
            employee.ifsc_code = ifsc_code or update_request.ifsc_code or employee.ifsc_code
            employee.bank_branch = bank_branch or update_request.bank_branch or employee.bank_branch
            employee.has_bank_account_edit = False

        try:
            employee.save()
            messages.success(request, 'Update request has been approved successfully.')

        except IntegrityError as e:
            messages.error(request, f'An error occurred while saving the employee profile: {e}')
            return redirect('admin_dashboard:employee_update_requests')
        
        except Exception as e:
            print(e)
            messages.error(request, 'An error occurred while saving the employee profile.')
            return redirect('admin_dashboard:employee_update_requests')
        
    elif action == 'reject':
        # Revert the flags in employee profile if the request is rejected
        if update_request.profile_edit:
            employee.has_profile_edit = False

        if update_request.bank_edit:
            employee.has_bank_account_edit = False

        # Save the employee profile with reverted changes
        try:
            employee.save()
            messages.success(request, 'Update request has been rejected.')
        except IntegrityError as e:
            messages.error(request, f'An error occurred while saving the employee profile: {e}')
            return redirect('admin_dashboard:employee_update_requests')
        
        except Exception as e:
            print(e)
            messages.error(request, 'An error occurred while saving the employee profile.')
            return redirect('admin_dashboard:employee_update_requests')

    # Delete the update request after either approving or rejecting
    update_request.delete()

    # Redirect back to the manage update requests page
    return redirect('admin_dashboard:employee_update_requests')


@group_required('hr')
def search_supervisor(request):
    search_query = request.GET.get('query', '')
    print("Search query:", search_query)
    if search_query:
        search_results = Employee.objects.filter(
            first_name__icontains=search_query
        ) | Employee.objects.filter(last_name__icontains=search_query)

        results = [
            {
                "id": result.employee_id,
                "name": f"{result.first_name} {result.last_name}",
                "designation": result.designation.designation_name if result.designation else 'N/A',  # Ensure the designation field exists
                "department": result.department.department_name if result.department else 'N/A'  # Ensure the department field exists
            } for result in search_results
        ]
        return JsonResponse({"results": results})
    return JsonResponse({"results": []})


@group_required('hr')
def manage_departments_and_designations(request):
    departments = Department.objects.all()
    designations = Designation.objects.all()
    context = {
        'departments': departments,
        'designations': designations,
    }
    return render(request, 'admin_dashboard/manage_departments_and_designations.html', context)

@group_required('hr')
def add_department(request):
    if request.method == 'POST':
        dept_name = request.POST.get('department_name')

        # Check if department like this already exists
        if Department.objects.filter(department_name=dept_name).exists():
            messages.error(request, 'Department with this name already exists.')
        else:
            Department.objects.create(department_name=dept_name)
            messages.success(request, 'Department added successfully.')
        return redirect('admin_dashboard:manage_departments_and_designations')
    
    return render(request, 'admin_dashboard/add_department.html')

@group_required('hr')
def add_designation(request):
    if request.method == 'POST':
        designation_name = request.POST.get('designation_name')
        responsibilities = request.POST.get('responsibilities')

        # Check if designation like this already exists
        if Designation.objects.filter(designation_name=designation_name).exists():
            messages.error(request, 'Designation with this name already exists.')
        else:
            Designation.objects.create(designation_name=designation_name, responsibilities=responsibilities)
            messages.success(request, 'Designation added successfully.')
        return redirect('admin_dashboard:manage_departments_and_designations')
    
    return render(request, 'admin_dashboard/add_designation.html')

