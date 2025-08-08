from django.shortcuts import redirect
from django.urls import reverse

class ForcePasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated and \
           request.user.profile.must_change_password and \
           request.path not in [reverse('password_change'), reverse('logout')]:
            return redirect(reverse('password_change'))
        return response