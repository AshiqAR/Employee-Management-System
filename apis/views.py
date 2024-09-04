from rest_framework import viewsets
from .serializers import EmployeeSerializer
from django.http import JsonResponse

from employees.models import Employee, Department, Designation, Roles
from attendance.models import Attendance

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer