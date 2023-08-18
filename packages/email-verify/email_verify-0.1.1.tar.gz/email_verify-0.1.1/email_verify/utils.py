from django.utils.timezone import now
from itsdangerous.url_safe import URLSafeTimedSerializer
from django.conf import settings
import json

def generate_token(user, domain=None):
    if domain is None and not settings.DEBUG:
        raise ValueError("Domain must be provided in production environment.")
    s = URLSafeTimedSerializer(settings.SECRET_KEY)
    str = s.dumps(json.dumps({'user_id': user.id, 'domain': domain}))
    return str


def verify_token(token):
    from .models import EmailVerification
    from itsdangerous import SignatureExpired, BadSignature
    s = URLSafeTimedSerializer(settings.SECRET_KEY)
    expires = getattr(settings, 'EMAIL_VERIFY_EXPIRES_IN', 3600)
    expires = expires if expires > 0 else None
    try:
        str = s.loads(token, max_age=expires)
        data = json.loads(str)
    except SignatureExpired:
        return (False, "Token has expired.")
    except BadSignature:
        return (False, "Invalid token.")

    domain = data.get('domain')
    user_id = data.get('user_id')
    
    if not settings.DEBUG and domain not in settings.ALLOWED_HOSTS:
        return (False, "Invalid domain.")

    if user_id:
        try:
            email_verification = EmailVerification.objects.get(user__id=user_id)
            if email_verification.is_verified:
                return (False, "Already verified.")
            
            email_verification.is_verified = True
            email_verification.verified_date = now()
            email_verification.save()
            return (True, None)
        except EmailVerification.DoesNotExist:
            return (False, "Email verification does not exist.")

    return (False, "Unknown error.")