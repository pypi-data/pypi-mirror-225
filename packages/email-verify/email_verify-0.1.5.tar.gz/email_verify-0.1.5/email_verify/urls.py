from django.urls import path
from . import views

app_name='email_verify'
urlpatterns = [
    path('verify_email/<str:token>/', views.EmailVerificationView.as_view(), name='verify_email'),
    path('email_verify/fail/',views.failure_view,name="verification_failure"),
    path('email_verify/success/',views.success_view,name="verification_success"),
]