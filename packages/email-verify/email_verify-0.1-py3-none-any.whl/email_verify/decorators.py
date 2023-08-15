from functools import wraps
from django.http import HttpResponseForbidden
from .models import EmailVerification

def user_verified(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            email_verification = EmailVerification.objects.get(user=user)
            if email_verification.is_verified or email_verification.verified_by_admin:
                return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("User email not verified.")

    return _wrapped_view