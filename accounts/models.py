from django.db import models
from django.contrib import auth
import uuid
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .managers import CustomUserManager

# Create your models here.
auth.signals.user_logged_in.disconnect(auth.models.update_last_login)


class CustomUser(AbstractUser):
    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, max_length=10)
    email = models.EmailField(_('email address'), unique=True)
    email_confirmed = models.BooleanField(default=False)
    # is_active = False
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

## Signal email_confirmed, set is_active True 

@receiver(pre_save, sender=CustomUser)
def update_user(sender, instance, **kwargs):
    if not instance.email_confirmed:
        instance.is_active = False
