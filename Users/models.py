# from django.db import models
# import uuid

# # Create your models here.

# class User(models.Model):
#     full_name = models.CharField(max_length=255)
#     username = models.CharField(max_length=100, unique=True)
#     password = models.CharField(max_length=100)
#     user_type = models.CharField(max_length=50)

#     def __str__(self):
#         return self.full_name


from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('manager', 'مدير'),
        ('operator', 'مشغل'),
    ]

    full_name = models.CharField(max_length=150)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return self.username
