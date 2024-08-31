from django.db import models
import uuid
from departments.models import Department
from django.contrib.auth.models import User

class Roles(models.TextChoices):
    HR = 'hr', 'HR'
    EMPLOYEE = 'employee', 'Employee'

class Designation(models.Model):
    designation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    designation_name = models.CharField(max_length=255)
    responsibilities = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.designation_name
    
class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    date_of_joining = models.DateField()
    address = models.CharField(default='No Address', max_length=255)
    has_profile_edit = models.BooleanField(default=False)

    emergency_contact_number = models.CharField(max_length=20)
    emergency_contact_name = models.CharField(max_length=255)
    emergency_contact_relationship = models.CharField(max_length=255, default='Emergency Contact')

    bank_name = models.CharField(max_length=255)
    bank_account_number = models.CharField(max_length=255)
    ifsc_code = models.CharField(max_length=11)
    bank_branch = models.CharField(max_length=255)
    has_bank_account_edit = models.BooleanField(default=False)

    experience_description = models.TextField()
    role = models.CharField(max_length=20, choices=Roles.choices, default='employee')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employees')
    supervisor = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subordinates')
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE)
    user_account = models.OneToOneField(User, on_delete=models.CASCADE)
    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Document(models.Model):
    document_id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=255)
    document_description = models.TextField()
    document_path = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    validated = models.BooleanField(default=False)

class EmployeeUpdate(models.Model):
    request_id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='update_requests')
    email = models.EmailField( default=None, blank=True, null=True)
    phone_number = models.CharField(max_length=20, default=None, blank=True, null=True)
    address = models.CharField(max_length=255, default=None, blank=True, null=True)
    emergency_contact_number = models.CharField(max_length=20, default=None, blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=255, default=None, blank=True, null=True)
    emergency_contact_relationship = models.CharField(max_length=255, default='Emergency Contact')
    profile_edit = models.BooleanField(default=False)

    bank_name = models.CharField(max_length=255, default=None, null=True, blank=True)
    bank_account_number = models.CharField(max_length=255, default=None, blank=True, null=True)
    ifsc_code = models.CharField(max_length=11, default=None, blank=True, null=True)
    bank_branch = models.CharField(max_length=255, default=None, blank=True, null=True)
    bank_edit = models.BooleanField(default=False)

    experience_description = models.TextField(default=None, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.employee_id.first_name + ' ' + self.employee_id.last_name
    
    def save(self, *args, **kwargs):
    # If profile_edit is True, mark the employee's profile as edited
        print("Saving EmployeeUpdate instance...")
        print("Initial data:", self.__dict__)
        if self.profile_edit:
            self.employee_id.has_profile_edit = True
            self.employee_id.save(update_fields=['has_profile_edit'])

        # If bank_edit is True, mark the employee's bank account as edited
        if self.bank_edit:
            self.employee_id.has_bank_account_edit = True
            self.employee_id.save(update_fields=['has_bank_account_edit'])

        # Populate fields with Employee data if not provided
        if self.email is None:
            self.email = self.employee_id.email
        if self.phone_number is None:
            self.phone_number = self.employee_id.phone_number
        if self.address is None:
            self.address = self.employee_id.address
        if self.emergency_contact_number is None:
            self.emergency_contact_number = self.employee_id.emergency_contact_number
        if self.emergency_contact_name is None:
            self.emergency_contact_name = self.employee_id.emergency_contact_name
        if self.emergency_contact_relationship is None:
            self.emergency_contact_relationship = self.employee_id.emergency_contact_relationship

        # Populate bank details if not provided
        if self.bank_name is None:
            self.bank_name = self.employee_id.bank_name
        if self.bank_account_number is None:
            self.bank_account_number = self.employee_id.bank_account_number
        if self.ifsc_code is None:
            self.ifsc_code = self.employee_id.ifsc_code
        if self.bank_branch is None:
            self.bank_branch = self.employee_id.bank_branch

        # Populate experience description if not provided
        if self.experience_description is None:
            self.experience_description = self.employee_id.experience_description

        # Call the parent save method to save the model
        super().save(*args, **kwargs)
        print("EmployeeUpdate saved with data:", self.__dict__)
