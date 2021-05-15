"""
Account Models
"""

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    username = models.CharField(max_length=254, null=True, blank=True, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    objects = UserManager()
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]
    
    def get_full_name(self):
        return self.name
