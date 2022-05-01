from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

    def is_valid(self):
        username = self.data.get('username')
        if User.objects.filter(username=username).exists():
            self.errors['__all__'] = [f'Username {username} already exists']
            return False
        return super(RegistrationForm, self).is_valid()
