from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

class EmailVerificationUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email')

    def clean_email(self):
        email = self.cleaned_data.get('email', None)
        if email:
            try:
                EmailValidator(message="Invalid e-mail")(email)
            except ValidationError as e:
                raise ValidationError("Invalid e-mail")
        return email

    def save(self, commit=True, request=None):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user