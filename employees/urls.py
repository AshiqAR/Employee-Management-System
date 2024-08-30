from django.urls import path
from . import views

app_name = 'employees'

urlpatterns = [
    path('', views.index, name='index'),
    path('change_password/', views.change_password, name='change_password'),
    path('my_account/', views.my_account_view, name='my_account'),
    path('notifications/', views.notifications_view, name='notifications'),

    path('logout/', views.logout_view, name='logout'),
]