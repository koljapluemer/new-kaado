from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Only used for confirmation or when you have to restore your password. Never sold, never spammed.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

    def get_credentials(self):
        return {
            "username": self.cleaned_data["username"],
            "password": self.cleaned_data["password1"]
        }
