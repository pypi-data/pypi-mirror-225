from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.utils.timezone import now
from django.dispatch import receiver
from .models import EmailVerification
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

@receiver(post_save, sender=User)
def create_email_verification(sender, instance=None, created=False, **kwargs):
    if created and not instance.is_superuser:
        ev = EmailVerification.objects.create(user=instance)
        try:
            ev.send_email()
            ev.last_email_date = now()
            ev.email_sent_status = True
            ev.save()
        except Exception as e:
            ev.last_email_date = now()
            ev.email_sent_status = False
            ev.save()
            raise e
            


@receiver(post_save, sender=User)
def save_email_verification(sender, instance=None, **kwargs):
    if not instance.is_superuser:
        instance.emailverification.save()


def check_email(sender, instance, **kwargs):
    email = instance.email
    if email and sender.objects.filter(email=email).exclude(username=instance.username).exists():
        raise ValidationError('Email Exists')


if getattr(settings, 'EMAIL_VERIFY_ENFORCE_UNIQUE_EMAILS', True):
    pre_save.connect(check_email, User)
