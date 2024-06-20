import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from users.manager import UserManager
from users.models_roles import Role


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    role_id = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    display_name = models.CharField(max_length=255, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True)
    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    objects = UserManager()

    def is_superuser(self):
        return self.role_id.id == "SPR"

    def is_admin(self):
        return self.role_id.id in ["ADM", "SPR"]

    def is_user(self):
        return self.role_id.id in ["USR", "ADM", "SPR"]

    def is_active(self):
        return self.status