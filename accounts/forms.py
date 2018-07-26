from django import forms
from django.contrib.auth.forms import UserCreationForm as AuthUserCreationForm

from . import models


class UserCreationForm(AuthUserCreationForm):

    username = forms.CharField(label='Username', required=True)
    email=forms.EmailField(label='Email',required=True)
    class Meta(AuthUserCreationForm.Meta):
        model = models.User

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data['email']
        if email and models.User.objects.filter(email=email).exists():
            self.add_error('email', 'Email already exists.')
        return cleaned_data


    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        user.email=self.cleaned_data['email']
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user