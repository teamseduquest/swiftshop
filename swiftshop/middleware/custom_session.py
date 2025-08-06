from django.conf import settings

class SplitSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            request.session_cookie_name = getattr(settings, 'ADMIN_SESSION_COOKIE_NAME', settings.SESSION_COOKIE_NAME)
        else:
            request.session_cookie_name = settings.SESSION_COOKIE_NAME

        response = self.get_response(request)

        # Set the cookie name on the response
        response.cookies[request.session_cookie_name] = request.session.session_key

        return response
