from django.db import models
import uuid
from employees.models import Employee
from datetime import timedelta, date

class LeaveType(models.TextChoices):
    SICK = 'sick', 'Sick'
    CASUAL = 'casual', 'Casual'
    VACATION = 'vacation', 'Vacation'

class LeaveStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'

class LeaveRequest(models.Model):
    leave_request_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=50, choices=LeaveType.choices)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    remarks = models.TextField(null=True, blank=True)  # For HR remarks
    status = models.CharField(max_length=50, choices=LeaveStatus.choices, default=LeaveStatus.PENDING)
    requested_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee} - {self.leave_type} request ({self.start_date} to {self.end_date})"
    
    @property
    def total_requested_days(self):
        """Exclude Sundays"""
        return calculate_total_leave_days(self.start_date, self.end_date)
    
    def approve_leave(self, approved_start_date, approved_end_date, remarks=None):
        """
        Mark the leave as approved, set the reviewed date, and create a Leave record.
        """
        # Create a Leave record upon approval
        Leave.objects.create(
            leave_request=self,
            employee=self.employee,
            leave_type=self.leave_type,
            requested_start_date=self.start_date,
            requested_end_date=self.end_date,
            approved_start_date=approved_start_date,
            approved_end_date=approved_end_date,
            status=LeaveStatus.APPROVED
        )
        # Remove the LeaveRequest instance after approval
        self.delete()

    def reject_leave(self, remarks=None):
        self.status = LeaveStatus.REJECTED
        self.reviewed_at = date.today()
        self.remarks = remarks
        self.save()

class Leave(models.Model):
    leave_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    leave_request = models.OneToOneField(LeaveRequest, on_delete=models.SET_NULL, related_name='leave', null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leaves')
    leave_type = models.CharField(max_length=50, choices=LeaveType.choices)
    requested_start_date = models.DateField()
    requested_end_date = models.DateField()
    approved_start_date = models.DateField()
    approved_end_date = models.DateField()
    remarks = models.TextField(null=True, blank=True)  # For HR remarks
    status = models.CharField(max_length=50, choices=LeaveStatus.choices, default=LeaveStatus.APPROVED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee} - {self.leave_type} ({self.requested_start_date} to {self.requested_end_date})"
    
    @property
    def total_leave_days(self):
        """Calculate total leave days excluding Sundays."""
        return calculate_total_leave_days(self.approved_start_date, self.approved_end_date)

def calculate_total_leave_days(start_date, end_date):
    """
    Function to calculate the total leave days between two dates, excluding Sundays.
    """
    delta = end_date - start_date
    total_days = 0
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        if day.weekday() != 6:
            total_days += 1
    return total_days
