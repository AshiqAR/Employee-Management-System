# basic URL Configurations
from django.urls import include, path
# import routers
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r'employees', views.EmployeeViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]