from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class Provider(models.TextChoices):
    GOOGLE = "google", "Google"
    APPLE = "apple", "Apple"


class UserManager(BaseUserManager):
    def create_user(self, email, sub, provider=None, password=None):
        user = self.model(email=email, sub=sub, provider=provider)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, sub, password=None):
        user = self.create_user(email=email, sub=sub, password=password, provider=None)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=255, null=True, blank=True)
    provider = models.CharField(
        max_length=20, choices=Provider.choices, null=True, blank=True
    )
    sub = models.CharField(max_length=255, unique=True, db_index=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "sub"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return f"{self.email or 'No email'} ({self.provider})"
