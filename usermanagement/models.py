import uuid
from datetime import timedelta

from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Time the activation is valid, in hours
VALID_TIME = 48


class UserTokenManager(models.Manager):
    def prune_expired(self):
        self.filter(created__lt=timezone.now() - timedelta(hours=VALID_TIME)).delete()


class UserToken(models.Model):
    user = models.ForeignKey(User)
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = UserTokenManager()

    # Activates the user and deletes the authentication object
    def activate(self):
        self.user.is_active = True
        self.user.save()
        self.delete()

    # Set the password and deletes the authentication object
    def set_password(self, password):
        self.user.set_password(password)
        self.user.save()
        self.delete()

    # Checks if the authentication object is expired
    def expired(self):
        return not timezone.now() < timedelta(hours=VALID_TIME) + self.created
