from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Submit


class LoginForm(forms.Form):
    class Meta:
        model = CustomUser
        fields = ('email', 'password')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        # Add placeholder and class in input
        self.fields['email'].widget.attrs.update({'class': 'input', 'placeholder': 'Email@gmail.com'})
        self.fields['password'].widget.attrs.update({'class': 'password', 'placeholder': 'Parol'})


class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        # Add placeholder and class in input
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email@gmail.com'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Parol'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Parol'})
        # Add label
        self.fields['username'].label = "Foydalanuvchi nomi"
        self.fields['email'].label = "Elektron pochta"
        self.fields['password1'].label = "Parol"
        self.fields['password2'].label = "Parolni tasdiqlang"


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'phone_nubmer', 'tg_username',)
