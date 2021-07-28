from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Slot(models.Model):
    user = models.ForeignKey(User,
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=255, default="AX")
    status = models.BooleanField(default=False)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        if self.number:
            return f'Slot <{self.number}>'
        return 'Slot <{self.pk}>'