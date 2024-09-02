from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('my_account/', views.my_account_view, name='my_account'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('add_attendance/', views.add_attendance, name='add_attendance'),
    path('leave_requests/', views.leave_requests, name='leave_requests'),
    path('notifications/', views.notifications, name='notifications'),
    path('logout/', views.logout_view, name='logout'),

    path('departments/', views.manage_departments_and_designations, name='manage_departments_and_designations'),
    path('add_department/', views.add_department, name='add_department'),
    path('add_designation/', views.add_designation, name='add_designation'),

    path('edit_employee/<int:employee_id>/', views.edit_employee, name='edit_employee'),
    path('search_supervisor/', views.search_supervisor, name='search_supervisor'),
    
    path('leave/review_leave_request/<uuid:leave_request_id>/', views.review_leave_request, name='review_leave_request'),
    path('employee_details/<int:employee_id>/', views.employee_details, name='employee_details'),
    path('employee_update_requests/', views.employee_update_requests, name='employee_update_requests'),

    path('handle_employee_update_request/<int:request_id>/', views.handle_employee_update_request, name='handle_employee_update_request'),
    path('validate_document/<int:document_id>/', views.handle_document_validation, name='handle_document_validation'),
]