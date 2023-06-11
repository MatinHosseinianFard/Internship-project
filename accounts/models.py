from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    address = models.TextField(blank=True)
    age = models.PositiveSmallIntegerField(blank=True, null=True)
    description = models.TextField(blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.username
