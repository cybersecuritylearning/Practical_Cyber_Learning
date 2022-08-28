from django.db import models

# Create your models here.

class UserToken(models.Model):
    UserId = models.CharField(max_length=128)
    Score = models.IntegerField()
    Time_to_live = models.TimeField()

def __str__(self):
    return self.UserId