from django.db import models

from django.db.models import Func, Q
from django.contrib.postgres.fields import HStoreField
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
from django.contrib.postgres.fields import IntegerRangeField

# Create your models here.
class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=13)
    email = models.CharField(max_length=75)
    content = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return 'Message from ' + self.name
