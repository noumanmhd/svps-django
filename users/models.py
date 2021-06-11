from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

def sub_routine():
    return timezone.now() + timedelta(days=30)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=255, null=True, blank=True)
    plate = models.CharField(max_length=255, null=True, blank=True, unique=True)
    cnic = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    subscription = models.DateTimeField(default=sub_routine)
    res_time =  models.DateTimeField(default=timezone.now)
    res_slot = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        if self.user.username:
            return f'Profile <{self.user.username}>'
        return 'Profile <{self.pk}>'

