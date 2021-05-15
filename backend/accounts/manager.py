"""
User Manager
"""

from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.utils import timezone


class UserManager(BaseUserManager):
    def _create_user(
        self, 
        email, 
        password, 
        is_staff, 
        is_superuser, 
        is_admin, 
        **extra_fields
    ):
        if not email:
            raise ValueError("Users must have an email address")
        now = timezone.now()
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            is_admin=is_admin,
            last_login=now,
            date_joined=now,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(
            email, password, False, False, False, **extra_fields
        )

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(
            email, password, True, True, True, **extra_fields
        )
        user.save(using=self._db)
        return user

    def create_admin(self, email, password, **extra_fields):
        user = self._create_user(
            email, password, False, True, True, **extra_fields
        )
        user.save(using=self._db)
        return user