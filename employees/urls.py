from django.urls import path
from . import views

app_name = 'employees'

urlpatterns = [
    path('', views.index, name='index'),
    path('change_password/', views.change_password, name='change_password'),
    path('my_account/', views.my_account_view, name='my_account'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('view_profile/', views.view_profile_view, name='view_profile'),
    path('update-personal-details/', views.update_personal_details, name='update_personal_details'),
    path('update-bank-details/', views.update_bank_details, name='update_bank_details'),
    path('upload-document/', views.upload_document, name='upload_document'),
    path('leave_application/', views.leave_application_view, name='leave_applications'),

    path('logout/', views.logout_view, name='logout'),
]