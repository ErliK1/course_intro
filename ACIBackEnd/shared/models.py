from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class ACIManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class ACIModel(models.Model):
    class Meta:
        app_label = 'shared'
        abstract = True

    deleted = models.BooleanField(default=False)


class User(AbstractUser):
    class Meta:
        db_table = 'auth_user'

    phone_number = models.CharField(max_length=100, null=True, blank=True)
    personal_number = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    
class ACIAdmin(models.Model):
    class Meta:
        db_table = 'aci_admin'
        
    user = models.OneToOneField(User, related_name='aci_admin', on_delete=models.CASCADE)
    
