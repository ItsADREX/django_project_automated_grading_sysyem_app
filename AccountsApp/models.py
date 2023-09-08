from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('STUDENT', 'Student'),
        ('INSTRUCTOR', 'Instructor'),
    )
    user_type = models.CharField(choices=USER_TYPE_CHOICES, max_length=10)
    matric_number = models.CharField(max_length=10, blank=True, null=True)
