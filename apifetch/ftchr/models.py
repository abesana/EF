from django.db import models

class ProfileModel(models.Model):
    network = models.CharField(max_length=32)
    username = models.CharField(max_length=128)
    count = models.IntegerField()
    description = models.CharField(max_length=1024 * 1024)

    class Meta:
        unique_together = ('network', 'username')

    def __unicode__(self):
        return "(network={0}, username={1})".format(self.network, self.username)
