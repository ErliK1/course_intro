from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.__str__()


class Event(models.Model):
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    date = models.DateTimeField()
    duration = models.DurationField()
    capacity = models.PositiveIntegerField(default=100)
    current_capacity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='pics')

    def __str__(self):
        return self.title.__str__()


class Perdorues(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.__str__()

class PerdoruesJoinsEvent(models.Model):
    perdorues = models.ForeignKey(Perdorues, on_delete=models.CASCADE, unique=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, unique=False)

    class Meta:
        unique_together = ('perdorues', 'event',)
    def __str__(self):
        return self.perdorues.__str__() + ' ' + self.event.__str__()





