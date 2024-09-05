from rest_framework import serializers
from employees.models import Employee, Roles
from attendance.models import Attendance

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['employee_id', 'first_name', 'last_name', 'email', 'phone_number', 'department', 'designation', 'date_of_joining']
        depth = 1

class AttendanceEmployeeDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['employee_id', 'date', 'attendance_type', 'work_type', 'shift', 'is_overtime', 'overtime_hours']
        labels = {
            'employee_id': 'employee',
        }
        depth = 1
