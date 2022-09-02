from django.db import models
from django_mysql.models import ListCharField


# Create your models here.

class UserToken(models.Model):
    UserId = models.CharField(max_length=128)
    Score = models.IntegerField()
    Time_to_live = models.TimeField()
    Passed_modules = ListCharField(
        base_field=models.CharField(max_length=11),
        size=11,
        max_length=(11 * 12),  # 6 * 10 character nominals, plus commas
    )


def __str__(self):
    return self.UserId