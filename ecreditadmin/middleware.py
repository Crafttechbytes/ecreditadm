from django.shortcuts import redirect
from django.urls import reverse


class RedirectIfLoggedInMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if hasattr(request, 'user') and request.user.is_authenticated:
            # If user is logged in and tries to access login, mainpage or signup page, redirect to dashboard
            if request.path in [reverse('login'), reverse('main')]:
                return redirect('dashboard')  # Change 'dashboard' to the actual URL name of your dashboard

        return response


class NoAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(reverse('admin:index')) and not request.user.is_staff:
            return redirect('login')  # Redirect non-staff users to the home page
        return self.get_response(request)
