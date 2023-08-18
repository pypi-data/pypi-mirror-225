from django.http import HttpResponseForbidden
from .models import EmailVerification

class UserVerifiedMixin:
    def verify_user_email(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            email_verification = EmailVerification.objects.get(user=user)
            if email_verification.is_verified:
                return None
        return HttpResponseForbidden("User email not verified.")

    def dispatch(self, request, *args, **kwargs):
        response = self.verify_user_email(request, *args, **kwargs)
        if response:
            return response # If there's an issue, return the forbidden response
        return super().dispatch(request, *args, **kwargs)