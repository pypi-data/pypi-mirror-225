from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.forms import ValidationError
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from .email_utils import send_verification_email, default_send_email

class UserCreationFormWithEmailValidation(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email')
    def save(self, commit=True, request=None):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Send the verification email
            #send_verification_email(user, send_email_func=settings.EMAIL_VERIFY_SEND_FUNC, request=request)
            send_verification_email(user, send_email_func=getattr(settings, 'EMAIL_VERIFY_SEND_FUNC', default_send_email), request=request)
            # Redirect to the verification sent page
            return redirect(reverse('email_verify:email_verification_sent'))
        return user
    def is_valid(self) -> bool:
        # Django's internal validations first
        is_form_valid = super().is_valid()
        # Then we get the submitted data
        email = self.cleaned_data.get('email', None)
        if email and is_form_valid:
            try:
                EmailValidator("Invalid e-mail")(email)
            except ValidationError:
                return False
            return True
        return False