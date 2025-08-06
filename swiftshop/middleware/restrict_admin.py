from django.shortcuts import redirect
from django.urls import reverse

class RestrictAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/') and request.user.is_authenticated and not request.user.is_staff:
            # return redirect(reverse('admin_dashboard'))  # or home page
            pass
        return self.get_response(request)
