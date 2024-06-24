from django.shortcuts import redirect
from django.contrib import messages


def user_verified(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.Profile.status:
            messages.warning(request, 'Please verify your email before loging in.')
            return redirect('auth-email')  # Redirect to the email confirmation page
        return view_func(request, *args, **kwargs)

    return wrapper
