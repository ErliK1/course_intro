from django.db import models

from django.contrib.auth.models import User



# Create your models here.

class Manager(models.Model):
    class Meta:
        db_table = 'manager'

    user = models.OneToOneField(User, related_name="ict_manager", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', null=True, blank=True)


class Visitor(models.Model):
    class Meta:
        db_table = 'visitor'

    user = models.OneToOneField(User, related_name='visitor', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

