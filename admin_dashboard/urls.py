from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('view_employees/', views.view_employees, name='view_employees'),
    path('add_attendance/', views.add_attendance, name='add_attendance'),
    path('leave_requests/', views.leave_requests, name='leave_requests'),
    path('notifications/', views.notifications, name='notifications'),
    path('logout/', views.logout_view, name='logout'),

    path('edit_employee/<int:employee_id>/', views.edit_employee, name='edit_employee'),
]