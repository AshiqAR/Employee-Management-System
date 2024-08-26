from django.contrib import admin
from .models import Employee, Designation, Document

admin.site.register(Designation)
admin.site.register(Employee)
admin.site.register(Document)
# Register your models here.
