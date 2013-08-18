from django.db import models

class ProfileModel(models.Model):
    network = models.CharField(max_length=32)
    username = models.CharField(max_length=128)
    count = models.IntegerField()
    description = models.CharField(max_length=1024 * 1024)
