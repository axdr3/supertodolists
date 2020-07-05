from django.db import models
from django.contrib import auth
import uuid
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager

# Create your models here.
auth.signals.user_logged_in.disconnect(auth.models.update_last_login)


class CustomUser(AbstractUser):
    username = None
    pk = None
    email = models.EmailField(_('email address'), unique=True)
    # token = models.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Token(models.Model):
	email = models.EmailField()
	uid = models.CharField(default=uuid.uuid4, max_length=20)
