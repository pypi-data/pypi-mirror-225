from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import EmailVerification
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def create_email_verification(sender, instance=None, created=False, **kwargs):
    print('We hear you')
    # we do not want this logic to run when `createsuperuser` is used
    if created and not instance.is_superuser:
        EmailVerification.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_email_verification(sender, instance=None, **kwargs):
    print('At least i hear you')
    if not instance.is_superuser:
        instance.emailverification.save()

@receiver(pre_save, sender=EmailVerification)
def verified_via_admin(sender,instance=None,**kwargs):
    if instance and instance.verified_by_admin:
        instance.is_verified = True