from django.db import models
from django_mysql.models import ListCharField
from django.contrib.auth.models import User


# Create your models here.

class UserToken(models.Model):
    UserId = models.CharField(max_length=128)
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    Score = models.IntegerField()
    Current_Level = models.CharField(max_length=128)
    Hash_check = models.CharField(max_length=64)

    Passed_modules = ListCharField(
        base_field=models.CharField(max_length=11),
        size=11,
        max_length=(11 * 12),  # 6 * 10 character nominals, plus commas
    )


def __str__(self):
    return self.UserId

class Learning_Modules(models.Model):
    Module_name = models.CharField(max_length=128)
    Module_message = models.TextField(blank=True)
    Module_tips = models.TextField(blank=True)
    Module_type = models.CharField(max_length=30)

def __str__(self):
    return self.Module_name