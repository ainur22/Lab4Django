from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, ContactRequest


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "auth-input",
            "placeholder": "Email енгізіңіз"
        })
    )

    class Meta:
        model = CustomUser
        fields = ["username", "email", "bio", "profile_image", "password1", "password2"]

        widgets = {
            "username": forms.TextInput(attrs={
                "class": "auth-input",
                "placeholder": "Мысалы: ainur2025"
            }),
            "bio": forms.Textarea(attrs={
                "class": "auth-input auth-textarea",
                "placeholder": "Өзіңіз туралы қысқаша жазыңыз",
                "rows": 3
            }),
            "profile_image": forms.ClearableFileInput(attrs={
                "class": "auth-input"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password1"].widget.attrs.update({
            "class": "auth-input",
            "placeholder": "Құпия сөз"
        })

        self.fields["password2"].widget.attrs.update({
            "class": "auth-input",
            "placeholder": "Құпия сөзді қайталау"
        })


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            "class": "auth-input",
            "placeholder": "Username немесе email енгізіңіз"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "auth-input",
            "placeholder": "Құпия сөз енгізіңіз"
        })
    )


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "bio", "profile_image"]

        widgets = {
            "username": forms.TextInput(attrs={
                "class": "profile-input",
                "placeholder": "Пайдаланушы аты"
            }),
            "email": forms.EmailInput(attrs={
                "class": "profile-input",
                "placeholder": "Email"
            }),
            "bio": forms.Textarea(attrs={
                "class": "profile-textarea",
                "placeholder": "Өзіңіз туралы",
                "rows": 5
            }),
            "profile_image": forms.ClearableFileInput(attrs={
                "class": "profile-input"
            }),
        }


class ContactRequestForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ["name", "phone", "question"]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "contact-input",
                "placeholder": "Аты-жөніңіз"
            }),
            "phone": forms.TextInput(attrs={
                "class": "contact-input",
                "placeholder": "+7 (777) 777 77 77"
            }),
            "question": forms.Textarea(attrs={
                "class": "contact-textarea",
                "placeholder": "Сұрағыңызды жазыңыз"
            }),
        }
