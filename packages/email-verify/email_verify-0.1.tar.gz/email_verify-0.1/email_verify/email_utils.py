from .utils import generate_token
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

def send_verification_email(user, send_email_func, request=None):
    current_site = get_current_site(request)
    domain = current_site.domain
    token = generate_token(user, domain=domain)
    verification_link = request.build_absolute_uri(reverse('email_verify:verify_email', args=[token]))

    send_email_func(user, verification_link)

def default_send_email(user, verification_link):
    from django.core.mail import send_mail
    from django.conf import settings
    subject = getattr(settings, 'EMAIL_VERIFY_SUBJECT_LINE','Email Verification')
    message = 'If you can\'t display the link, copy and paste this into your browser\'s address bar: {verification_link}'
    html_message = getattr(settings, 'EMAIL_VERIFY_MESSAGE',f'Verify your email by clicking the link: <br><a href="{verification_link}" style="background-color: #2196F3; color: white; text-align: center; padding: 8px 15px; text-decoration: none; display: inline-block; font-family: Arial, sans-serif; font-size: 16px; border-radius: 4px;">Verify your email</a><br>If you can\'t display the link copy and paste this into your browser\'s address bar: {verification_link}')
    from_email = getattr(settings,'EMAIL_VERIFY_FROM_ADDRESS','verify@email_verify.com')
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list, html_message=html_message)