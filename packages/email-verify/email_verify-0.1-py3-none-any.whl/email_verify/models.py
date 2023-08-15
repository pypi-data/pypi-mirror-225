from django.contrib.auth.models import User
from django.db import models

class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    verified_by_admin = models.BooleanField(default=False) # Allow anyone using admin panel to set verification status