from django.db import models
from django.contrib.auth.models import AbstractUser
import os


def user_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"avatar.{ext}"
    return os.path.join("users", instance.username, filename)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(
        upload_to=user_avatar_path,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username


class ContactRequest(models.Model):
    name = models.CharField(max_length=120, verbose_name="Аты")
    phone = models.CharField(max_length=30, verbose_name="Телефон")
    question = models.TextField(verbose_name="Сұрақ")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.phone}"