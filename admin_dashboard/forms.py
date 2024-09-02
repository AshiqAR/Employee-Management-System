from django import forms
from departments.models import Department
from employees.models import Employee, Designation

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department_name']
        widgets = {
            'department_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
    department_id = forms.UUIDField(required=False, widget=forms.HiddenInput())

from django import forms
from .models import Employee, Designation

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'first_name', 'last_name', 'email', 'phone_number', 
            'date_of_birth', 'date_of_joining', 'bank_name', 
            'bank_account_number', 'ifsc_code', 'department', 
            'designation', 'role'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_of_joining': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_account_number': forms.TextInput(attrs={'class': 'form-control'}),
            'ifsc_code': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'designation': forms.Select(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'phone_number': 'Phone Number',
            'date_of_birth': 'Date of Birth',
            'date_of_joining': 'Date of Joining',
            'bank_name': 'Bank Name',
            'bank_account_number': 'Bank Account Number',
            'ifsc_code': 'IFSC Code',
            'department': 'Department',
            'designation': 'Designation',
            'role': 'Role',
        }

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        # Populate the designation field with available designations
        self.fields['designation'].queryset = Designation.objects.all()
        self.fields['department'].queryset = Department.objects.all()
        
