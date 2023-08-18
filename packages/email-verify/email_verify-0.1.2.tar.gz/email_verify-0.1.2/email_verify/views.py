from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from .utils import verify_token

class EmailVerificationView(View):
    success_url = reverse_lazy('email_verify:verification_success')
    failure_url = reverse_lazy('email_verify:verification_failure')

    def get(self, _, token):
        success, message = verify_token(token)
        
        if success:
            return HttpResponseRedirect(self.success_url)
        else:
            return HttpResponseRedirect(self.failure_url + f"?message={message}")
        
def failure_view(request):
    message = request.GET.get('message', 'An error occurred.')
    return render(request, 'email_verify/failure.html', {'message': message})

def success_view(request):
    main_page = getattr(settings,'MAIN_PAGE','/')
    return render(request, 'email_verify/success.html',{'main_page':main_page})