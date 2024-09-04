from typing import Any
from django import forms
from departments.models import Department
from employees.models import Employee, Designation
from attendance.models import Attendance, Shift, AttendanceType, WorkType

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department_name']
        widgets = {
            'department_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
    department_id = forms.UUIDField(required=False, widget=forms.HiddenInput())

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
        self.fields['designation'].queryset = Designation.objects.all()
        self.fields['department'].queryset = Department.objects.all()
        self.fields['department'].label_from_instance = lambda obj: obj.department_name

    def save(self, commit=True, user_account=None):
        employee = super().save(commit=False)
        if user_account:
            employee.user_account = user_account
        if commit:
            employee.save()
        return employee


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['date', 'attendance_type', 'work_type', 'shift', 'is_overtime', 'overtime_hours']

    # Adding additional widgets and customization
    date = forms.DateField(widget=forms.SelectDateWidget)
    attendance_type = forms.ChoiceField(choices=AttendanceType.choices, widget=forms.Select)
    work_type = forms.ChoiceField(choices=WorkType.choices, widget=forms.Select)
    shift = forms.ModelChoiceField(queryset=Shift.objects.all(), widget=forms.Select)
    is_overtime = forms.BooleanField(required=False)
    overtime_hours = forms.IntegerField(min_value=0, max_value=8, required=False)
