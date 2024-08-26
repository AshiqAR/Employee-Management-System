from django.db import models
import uuid
from employees.models import Employee
from enum import Enum

class WorkType(models.TextChoices):
    WORK_FROM_HOME = 'WorkFromHome', 'Work From Home'
    WORK_FROM_OFFICE = 'WorkFromOffice', 'Work From Office'

class AttendanceType(models.TextChoices):
    FULL_DAY = 'FullDay', 'Full Day'
    HALF_DAY = 'HalfDay', 'Half Day'

class Shift(models.Model):
    shift_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shift_name = models.CharField(max_length=255)
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Create your models here.
class Attendance(models.Model):
    attendance_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    check_in_time = models.DateTimeField()
    check_out_time = models.DateTimeField()
    attendance_type = models.CharField(max_length=50, choices=AttendanceType.choices)
    work_type = models.CharField(max_length=50, choices=WorkType.choices)
    shift = models.ForeignKey('Shift', on_delete=models.CASCADE)
    is_overtime = models.BooleanField(default=False)
    overtime_hours = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)