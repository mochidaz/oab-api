import uuid

from django.contrib.auth.base_user import BaseUserManager

from users.models_roles import Role


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        id = uuid.uuid4()
        user = self.model(id=id, username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        role = Role.objects.get(id="SPR")
        extra_fields.setdefault('role_id', role)
        return self.create_user(username, email, password, **extra_fields)