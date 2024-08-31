from django.contrib import admin
from .models import Employee,EmployeeUpdate, Designation, Document

admin.site.register(Designation)
admin.site.register(Employee)
admin.site.register(Document)
admin.site.register(EmployeeUpdate)
# Register your models here.
