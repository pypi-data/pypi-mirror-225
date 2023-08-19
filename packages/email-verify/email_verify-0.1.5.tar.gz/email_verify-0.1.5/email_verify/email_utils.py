import logging
import smtplib
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
from .utils import generate_token
from .exceptions import TokenGenerationException, EmailSendingException, InvalidDomainException


def default_send_email(user, verification_link):
    from django.core.mail import send_mail
    from django.conf import settings
    subject = getattr(settings, 'EMAIL_VERIFY_SUBJECT_LINE','Email Verification')
    message = getattr(settings, 'EMAIL_VERIFY_TEXT_MESSAGE','If you can\'t display the link, copy and paste this into your browser\'s address bar: $:_VERIFICATION_LINK')
    html_message = getattr(settings, 'EMAIL_VERIFY_HTML_MESSAGE',f'Verify your email by clicking the link: <br><a href="$:_VERIFICATION_LINK" style="background-color: #2196F3; color: white; text-align: center; padding: 8px 15px; text-decoration: none; display: inline-block; font-family: Arial, sans-serif; font-size: 16px; border-radius: 4px;">Verify your email</a><br>If you can\'t display the link copy and paste this into your browser\'s address bar: $:_VERIFICATION_LINK')
    from_email = getattr(settings,'EMAIL_VERIFY_FROM_ADDRESS','verify@email_verify.com')
    recipient_list = [user.email]
    send_mail(subject, message.replace('$:_VERIFICATION_LINK',verification_link), from_email, recipient_list, html_message=html_message.replace('$:_VERIFICATION_LINK',verification_link))
    
def send_verification_email(user, send_email_func, request=None,domain=None):
    if not domain:
        # Use the request object if provided, otherwise fall back to ALLOWED_HOSTS
        if request:
            current_site = get_current_site(request)
            domain = current_site.domain
            port = request.get_port()
            if port not in ('80', '443'):
                domain += f":{port}"
        else:
            if settings.DEBUG:
                domain = settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost'
                domain = 'localhost' if domain == '*' else domain
                port = settings.DEBUG_PORT if hasattr(settings, 'DEBUG_PORT') else '8000'
                domain += f":{port}"
            elif settings.ALLOWED_HOSTS:
                domain = settings.ALLOWED_HOSTS[0]
            else:
                raise InvalidDomainException("Couldn't resolve domain for token. If DEBUG is set to false ALLOWED_HOSTS[0] must be set or request object should be passed to function send_verification_email")
    
    try:
        token = generate_token(user, domain=domain)
    except Exception as e:
        logging.error(f"Problem generating token: {e}")
        raise TokenGenerationException("An error occurred while generating token") from e

    if request:
        verification_link = request.build_absolute_uri(reverse('email_verify:verify_email', args=[token]))
    else:
        path = reverse('email_verify:verify_email', args=[token])
        protocol = 'https' if settings.SECURE_SSL_REDIRECT else 'http'
        verification_link = f"{protocol}://{domain}{path}"

    try:
        send_email_func(user, verification_link)
    except smtplib.SMTPException as e:
        logging.error(f"SMTP error occurred: {e}")
        raise EmailSendingException("An SMTP error occurred while sending email.") from e
    except Exception as e:
        # General catch-all for errors, especially if a user-provided email sending function is used
        logging.error(f"General email sending error occurred: {e}")
        raise EmailSendingException("An error occurred while sending email. Please refer to the logs for details.") from e

    
def send_verification_email_wrapper(user,request=None,domain=None):
    send_fn = getattr(settings,'EMAIL_VERIFY_SEND_FUNC', default_send_email)
    send_verification_email(user,send_fn,request,domain)