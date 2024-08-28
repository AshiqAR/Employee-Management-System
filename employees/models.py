from django.db import models
import uuid
from departments.models import Department
from django.contrib.auth.models import User

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
    address = models.TextField()
    emergency_contact_number = models.CharField(max_length=20)
    emergency_contact_name = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=255)
    bank_account_number = models.CharField(max_length=255)
    ifsc_code = models.CharField(max_length=11)
    experience_description = models.TextField()
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
    document_path = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    validated = models.BooleanField(default=False)

class EmployeeUpdate(models.Model):
    request_id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='update_requests')
    email = models.EmailField(unique=True, default=None)
    phone_number = models.CharField(max_length=20, unique=True, default=None)
    address = models.TextField(default=None)
    emergency_contact_number = models.CharField(max_length=20, default=None)
    emergency_contact_name = models.CharField(max_length=255, default=None)
    bank_name = models.CharField(max_length=255, default=None)
    bank_account_number = models.CharField(max_length=255, default=None)
    ifsc_code = models.CharField(max_length=11, default=None)
    experience_description = models.TextField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name