from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    """Custom manager for a user model without email."""

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The username must be set.")

        user = self.model(
            username=username,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(
            username=username,
            password=password,
            **extra_fields,
        )


class User(AbstractUser):
    email = None

    avatar = models.ImageField(
        upload_to="users/avatar/",
        blank=True,
        null=True,
    )

    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return self.username