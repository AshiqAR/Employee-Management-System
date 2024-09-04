from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Attendance, Employee
import json

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the attendance index.")


@csrf_exempt
@require_POST
def save_attendance(request):
    try:
        data = json.loads(request.body)

        employee_id = int(data.get('employee_id'))
        print(employee_id)
        date = data.get('date')
        attendance_status = data.get('attendance_status')
        overtime_hours = data.get('overtime_hours')

        if not employee_id or not date or not attendance_status:
            return JsonResponse({'error': 'Missing fields'}, status=400)

        try:
            employee = Employee.objects.get(employee_id=employee_id)
        except Employee.DoesNotExist:
            return JsonResponse({'error': 'Employee not found'}, status=404)
        
        attend = Attendance.objects.filter(employee_id=employee, date=date)
        if attend:
            print("Attendance already exists")
            return JsonResponse({'error': 'Attendance already exists'}, status=400)
        

        attendance = Attendance.objects.create(
            employee_id=employee,
            date=date,
            attendance_type=attendance_status,
            overtime_hours=overtime_hours or 0
        )

        return JsonResponse({'message': 'Attendance saved successfully'}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
