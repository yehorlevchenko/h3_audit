from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=63)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
