from django.db import models
from django.contrib.auth.models import AbstractUser
import os


def user_avatar_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"avatar.{ext}"
    return os.path.join("users", instance.username, filename)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to=user_avatar_path, blank=True, null=True)

    dark_mode = models.BooleanField(default=False)
    notifications = models.BooleanField(default=True)
    show_timer = models.BooleanField(default=True)
    shuffle_questions = models.BooleanField(default=False)
    ai_explanation = models.BooleanField(default=True)
    site_language = models.CharField(max_length=10, default="kk")

    def __str__(self):
        return self.username


class ContactRequest(models.Model):
    name = models.CharField(max_length=120, verbose_name="Аты")
    phone = models.CharField(max_length=30, verbose_name="Телефон")
    question = models.TextField(verbose_name="Сұрақ")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.phone}"


class AIChatSession(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="ai_chat_sessions")
    title = models.CharField(max_length=120, default="Жаңа чат")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class AIChatMessage(models.Model):
    ROLE_CHOICES = (
        ("user", "User"),
        ("bot", "Bot"),
    )

    chat = models.ForeignKey(AIChatSession, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.role}: {self.text[:40]}"