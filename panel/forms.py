from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=63)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=120, help_text='Required. Add a valid email address', required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')