from itsdangerous.url_safe import URLSafeTimedSerializer
from itsdangerous import SignatureExpired
from itsdangerous import timed
from django.conf import settings
from .models import EmailVerification
from .exceptions import *
import json

def generate_token(user, domain=None):
    if domain is None and not settings.DEBUG:
        raise ValueError("Domain must be provided in production environment.")
    s = URLSafeTimedSerializer(settings.SECRET_KEY)
    str = s.dumps(json.dumps({'user_id': user.id, 'domain': domain}))
    return str


def verify_token(token):
    s = URLSafeTimedSerializer(settings.SECRET_KEY)
    try:
        expires = getattr(settings,'EMAIL_VERIFY_EXPIRES_IN',3600)
        str = s.loads(token, max_age=expires)
        data = json.loads(str)
    except SignatureExpired:
        raise TokenExpired("Token has expired.")
    except:
        return None
    domain = data.get('domain')
    user_id = data.get('user_id')
    if not settings.DEBUG and domain not in settings.ALLOWED_HOSTS:
        raise InvalidDomain("Invalid domain.")
    if user_id:
        try:
            email_verification = EmailVerification.objects.get(user__id=user_id)
            if email_verification.is_verified:
                raise AlreadyVerified()
            email_verification.is_verified = True
            email_verification.save()
            return True
        except EmailVerification.DoesNotExist:
            return None
    return None