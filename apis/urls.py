# basic URL Configurations
from django.urls import include, path
# import routers
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r'employees', views.EmployeeViewSet)

app_name = 'apis'


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('attendance/<str:date>/', views.AttendanceByDateView.as_view(), name='get_attendance_by_date'),
    path('update-attendance/', views.UpdateAttendanceView.as_view(), name='update_attendance'),
]