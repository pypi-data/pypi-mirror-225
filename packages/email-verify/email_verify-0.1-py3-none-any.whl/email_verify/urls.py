from django.urls import path
from . import views

app_name = 'email_verify'
urlpatterns = [
    path('verify_email/<str:token>/', views.verify_email_view, name='verify_email'),
    path('email_verify/verification_success', views.verification_success, name='email_verification_success'),
    path('email_verify/verification_failed', views.verification_failed, name='email_verification_failed'),
    path('email_verify/resend_verification_email/', views.resend_verification_email_view, name='resend_verification_email'),
    path('email_verify/email_verification_resend_success/', views.email_verification_resend_success, name='email_verification_resend_success'),
    path('email_verify/email_verification_sent/', views.email_verification_sent, name='email_verification_sent'),

]