from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        login_url = reverse('users:login')
        print('inseide middleware')
        
        if request.path.startswith('/admin/') or request.path == login_url:
            return None
        
        if request.user.is_authenticated:
            print('User is authenticated')
        
        if not request.user.is_authenticated:
            print('User is not authenticated')
            return redirect(login_url)
        
        return None
