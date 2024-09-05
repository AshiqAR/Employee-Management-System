from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import EmployeeSerializer, AttendanceEmployeeDateSerializer
from django.http import JsonResponse
from datetime import datetime
from employees.models import Employee, Department, Designation, Roles
from attendance.models import Attendance

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class AttendanceByDateView(APIView):
    def get(self, request, date):
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'error': 'Invalid Date Format'}, status=400)
        
        employees = Employee.objects.filter(date_of_joining__lte=date_obj).select_related('department', 'designation')
        attendance_data = []

        for employee in employees:

            attendance_record = Attendance.objects.filter(employee_id=employee, date=date_obj).first()
            if attendance_record:
                serialized_attendance = AttendanceEmployeeDateSerializer(attendance_record)
                attendance_data.append({'attendance': serialized_attendance.data})
            else:
                attendance_data.append({
                    'employee': EmployeeSerializer(employee).data,
                    'attendance': {
                        'employee_id': employee.employee_id,
                        'date': date_obj,
                        'attendance_type': 'Absent',
                        'work_type': 'Absent',
                        'shift': None,
                        'is_overtime': False,
                        'overtime_hours': 0
                    }
                })
        return JsonResponse(attendance_data, safe=False)

class UpdateAttendanceView(APIView):
    def post(self, request):
        data = request.data
        employee_id = data.get('employee_id')
        date = data.get('date')
        attendance = data.get('attendance')

        if not employee_id or not date or not attendance:
            return JsonResponse({'error': 'Invalid Request'}, status=400)

        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'error': 'Invalid Date Format'}, status=400)
        
        try:
            employee = Employee.objects.get(employee_id=employee_id, joining_date__lte=date_obj)
        except Employee.DoesNotExist:
            return JsonResponse({'error': 'Employee not found'}, status=404)
        
        attendance_record = Attendance.objects.filter(employee_id=employee, date=date_obj).first()
        if attendance_record:
            attendance_record.attendance_type = attendance.get('attendance_type', attendance_record.attendance_type)
            attendance_record.work_type = attendance.get('work_type', attendance_record.work_type)
            attendance_record.shift_id = attendance.get('shift_id', attendance_record.shift_id)
            attendance_record.is_overtime = attendance.get('is_overtime', attendance_record.is_overtime)
            attendance_record.overtime_hours = attendance.get('overtime_hours', attendance_record.overtime_hours)
            attendance_record.save()
        else:
            attendance_record = Attendance.objects.create(
                employee_id=employee,
                date=date_obj,
                attendance_type=attendance.get('attendance_type'),
                work_type=attendance.get('work_type'),
                shift_id=attendance.get('shift_id'),
                is_overtime=attendance.get('is_overtime'),
                overtime_hours=attendance.get('overtime_hours')
            )
        
        return JsonResponse({'success': 'Attendance Updated Successfully'})