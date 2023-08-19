from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from .models import EmailVerification

def user_verified(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            email_verification = get_object_or_404(EmailVerification, user=user)
            if email_verification.is_verified:
                return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("User email not verified.")

    return _wrapped_view