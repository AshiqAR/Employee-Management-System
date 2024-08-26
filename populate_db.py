import datetime
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_management.settings')

import django
django.setup()

import random
from employees.models import Designation, Employee, Document
from departments.models import Department
from django.contrib.auth.models import User
from attendance.models import Attendance, Shift
from leave.models import LeaveRequest, Leave

from faker import Faker

fakegen = Faker()
departments = ['HR', 'IT', 'Finance', 'Operations', 'Sales']
job_responsibilities = [
    "Recruitment",
    "Training",
    "Employee Relations",
    "Performance Management",
    "Compensation and Benefits",
    "Employee Engagement",
    "Policy Formulation",
    "HR Operations",
    "HRIS",
    "Talent Management",
    "Succession Planning",
    "Change Management",
]
desig = [
    "HR Manager",
    "Software Developer",
    "DevOps Engineer",
    "Data Scientist",
    "Business Analyst",
    "Quality Analyst",
    "Sales Manager",
    "Finance Manager",
    "Operations Manager",
]

def add_department():
    d = Department.objects.get_or_create(department_name=random.choice(departments))[0]
    # d.save()
    return d

def add_designation():
    selected_responsibilities = random.sample(job_responsibilities, random.randint(2, 4))
    responsibilities_str = ', '.join(selected_responsibilities)
    
    d = Designation.objects.get_or_create(
        designation_name = random.choice(desig),
    )[0]
    
    d.responsibilities = responsibilities_str
    # d.save()
    return d

def add_employee():
    d = add_department()
    des = add_designation()
    
    first_name = fakegen.first_name()
    last_name = fakegen.last_name()
    email = fakegen.email()
    phone_number = fakegen.phone_number()
    date_of_birth = fakegen.date_of_birth()
    date_of_joining = fakegen.date_this_decade()
    address = fakegen.address()
    emergency_contact_number = fakegen.phone_number()
    emergency_contact_name = fakegen.name()
    bank_name = fakegen.company()
    bank_account_number = fakegen.credit_card_number(card_type=None)
    ifsc_code = fakegen.bban()
    experience_description = fakegen.text()
    department = d
    supervisor = None
    designation = des
    user_account = User.objects.create_user(
        username=email,
        email=email,
        password='password123'
    )
    created_at = fakegen.date_time_this_decade()

    e = Employee.objects.get_or_create(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
        date_of_birth=date_of_birth,
        date_of_joining=date_of_joining,
        address=address,
        emergency_contact_number=emergency_contact_number,
        emergency_contact_name=emergency_contact_name,
        bank_name=bank_name,
        bank_account_number=bank_account_number,
        ifsc_code=ifsc_code,
        experience_description=experience_description,
        department=department,
        supervisor=supervisor,
        designation=designation,
        user_account=user_account,
        created_at=created_at,
    )[0]
    e.save()
    print(e.employee_id)
    return e

def add_document():
    e = add_employee()
    document_type = fakegen.file_name()
    document_path = fakegen.file_path()
    uploaded_at = fakegen.date_time_this_decade()
    
    d = Document.objects.get_or_create(
        employee=e,
        document_type=document_type,
        document_path=document_path,
        uploaded_at=uploaded_at,
    )[0]
    # d.save()
    return d

shiftname = ['Day']
def add_shift():
    shift_name = random.choice(shiftname)
    start_time = fakegen.time()
    end_time = start_time + datetime.timedelta(hours=8)
    created_at = fakegen.date_time_this_decade()
    updated_at = fakegen.date_time_this_decade()
    
    s = Shift.objects.get_or_create(
        shift_name=shift_name,
        start_time=start_time,
        end_time=end_time,
        created_at=created_at,
        updated_at=updated_at,
    )[0]

    # s.save()
    return s

def add_attendance():
    # Get a random employee from the database
    e = Employee.objects.order_by('?').first()
    # Get a random shift from the database
    s = Shift.objects.order_by('?').first()

    date = fakegen.date_this_year()
    check_in_time = datetime.datetime.combine(date, s.start_time)
    check_out_time = datetime.datetime.combine(date, s.end_time)
    attendance_type = random.choice(['FullDay', 'HalfDay'])
    work_type = random.choice(['WorkFromHome', 'WorkFromOffice'])
    is_overtime = random.choice([True, False])
    created_at = fakegen.date_time_this_decade()
    updated_at = fakegen.date_time_this_decade()
    overtime_hours = is_overtime * random.randint(1, 4)

    a = Attendance.objects.get_or_create(
        employee_id = e.employee_id,
        date=date,
        check_in_time=check_in_time,
        check_out_time=check_out_time,
        attendance_type=attendance_type,
        work_type=work_type,
        shift=s,
        is_overtime=is_overtime,
        overtime_hours=overtime_hours,
        created_at=created_at,
        updated_at=updated_at,
    )[0]

    # a.save()
    return a

if __name__ == '__main__':
    print("Populating the database...Please wait")
    for _ in range(10):
        add_employee()