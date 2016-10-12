from django.conf import settings
from django.db import models
import pyotp


class UserPSK(models.Model):
    """Strores custom secret key per user"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='psk', on_delete=models.CASCADE)

    secret_key = models.CharField(max_length=16, default=pyotp.random_base32)
