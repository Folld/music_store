from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import resolve_url
from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from authorization.forms import RegistrationForm


class RegistrationView(generic.FormView):
    template_name = 'registration/registration.html'
    form_class = RegistrationForm

    def form_valid(self, form):
        User.objects.create_user(**form.cleaned_data)
        return HttpResponseRedirect(resolve_url(settings.LOGIN_REDIRECT_URL))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(resolve_url(request.GET.get('next') or settings.LOGIN_REDIRECT_URL))

