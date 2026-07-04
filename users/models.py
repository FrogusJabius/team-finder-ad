from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email")
    bio = models.TextField(blank=True, null=True, verbose_name="О себе")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    github = models.URLField(blank=True, null=True, verbose_name="GitHub")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")
    skills = models.ManyToManyField(Skill, related_name='users', blank=True, verbose_name="Навыки")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
