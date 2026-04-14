from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, ContactRequest


class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'bio', 'profile_image', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'bio', 'profile_image']

class ContactRequestForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['name', 'phone', 'question']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'contact-input',
                'placeholder': 'Аты-жөніңіз'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'contact-input',
                'placeholder': '+7 (777) 777 77 77'
            }),
            'question': forms.Textarea(attrs={
                'class': 'contact-textarea',
                'placeholder': 'Сұрағыңызды жазыңыз'
            }),
        }