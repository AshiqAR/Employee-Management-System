from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib import messages
from django import forms

from .forms import PersonalDetailsForm, BankDetailsForm
from django.contrib.auth.models import User
from .models import Employee, Document, EmployeeUpdate

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

def get_employee_profile_context(user):
    employee = get_object_or_404(Employee, user_account=user)
    employee_docs = Document.objects.filter(employee_id=employee.employee_id)
    
    updated_employee_personal = EmployeeUpdate.objects.filter(employee_id=employee).last()
    updated_employee_bank = EmployeeUpdate.objects.filter(employee_id=employee).last()
    
    context = {
        'employee': employee,
        'documents': employee_docs,
        'updated_employee_personal': updated_employee_personal,
        'updated_employee_bank': updated_employee_bank,
        'personal_form': PersonalDetailsForm(instance=employee),
        'bank_form': BankDetailsForm(instance=employee),
    }
    
    return context

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
                return redirect('employees:my_account')

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
                return redirect('employees:my_account')

    return render(request, 'employees/my_account.html', context)

@group_required('employee')
def notifications_view(request):
    return render(request, 'employees/notifications.html')

@group_required('employee')
def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('users:login')

@group_required('employee')
def view_profile_view(request):
    context = get_employee_profile_context(request.user)
    return render(request, 'employees/view_profile.html', context)

@group_required('employee')
def update_personal_details(request):
    employee = get_object_or_404(Employee, user_account=request.user)

    if request.method == 'POST':
        if employee.has_profile_edit:
            messages.error(request, 'You already have a pending request to update your personal details.')
            return redirect('employees:view_profile')
        
        form = PersonalDetailsForm(request.POST, instance=employee)
        if form.is_valid():
            update_fields = {}
            for field in form.cleaned_data:
                new_value = form.cleaned_data[field]
                old_value = getattr(employee, field)
                if new_value != old_value:
                    update_fields[field] = new_value
            
            if update_fields:
                # EmployeeUpdate.objects.create(
                #     employee_id=employee,
                #     email=update_fields.get('email', employee.email),
                #     phone_number=update_fields.get('phone_number', employee.phone_number),
                #     address=update_fields.get('address', employee.address),
                #     emergency_contact_name=update_fields.get('emergency_contact_name', employee.emergency_contact_name),
                #     emergency_contact_number=update_fields.get('emergency_contact_number', employee.emergency_contact_number),
                #     emergency_contact_relationship=update_fields.get('emergency_contact_relationship', employee.emergency_contact_relationship),
                # )
                # employee.has_profile_edit = True
                # employee.save()

                messages.success(request, 'Your personal details update has been saved and will be reflected after validation.')
            else:
                messages.info(request, 'No changes detected in your personal details.')

            return redirect('employees:view_profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    
    context = get_employee_profile_context(request.user)
    context['personal_form'] = form

    return render(request, 'employees/view_profile.html', context)

@group_required('employee')
def update_bank_details(request):
    employee = get_object_or_404(Employee, user_account=request.user)

    if request.method == 'POST':
        if employee.has_bank_edit:
            messages.error(request, 'You already have a pending request to update your bank details.')
            return redirect('employees:view_profile')
        
        form = BankDetailsForm(request.POST, instance=employee)
        if form.is_valid():
            update_fields = {}
            for field in form.cleaned_data:
                new_value = form.cleaned_data[field]
                old_value = getattr(employee, field)
                if new_value != old_value:
                    update_fields[field] = new_value
            
            if update_fields:
                EmployeeUpdate.objects.create(
                    employee_id=employee,
                    bank_name=update_fields.get('bank_name', employee.bank_name),
                    bank_account_number=update_fields.get('bank_account_number', employee.bank_account_number),
                    ifsc_code=update_fields.get('ifsc_code', employee.ifsc_code),
                    bank_branch=update_fields.get('bank_branch', employee.bank_branch),
                )
                employee.has_bank_edit = True
                employee.save()

                messages.success(request, 'Your bank details update has been saved and will be reflected after validation.')
            else:
                messages.info(request, 'No changes detected in your bank details.')

            return redirect('employees:view_profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    
    context = get_employee_profile_context(request.user)
    context['bank_form'] = form

    return render(request, 'employees/view_profile.html', context)


@group_required('employee')
def add_document(request):
    employee = get_object_or_404(Employee, user_account=request.user)

    if request.method == 'POST':
        document_type = request.POST.get('document_type')
        document_description = request.POST.get('document_description')
        document_path = request.POST.get('document_path')
        # Document.objects.create(employee_id=employee, document_type=document_type, document_description=document_description, document_path=document_path)
        messages.success(request, 'Document added successfully.')
        return redirect('employees:view_profile')
    
    return render(request, 'employees/add_document.html')



@group_required('employee')
def leave_application_view(request):
    return render(request, 'employees/leave_applications.html')