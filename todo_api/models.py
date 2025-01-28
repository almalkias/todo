from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High')
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=1,
        choices=PRIORITY_CHOICES,
        default='M'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    