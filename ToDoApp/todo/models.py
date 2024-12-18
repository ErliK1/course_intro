from django.db import models

# Create your models here.

gender_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
    )


class DailyTask(models.Model):
    class Meta:
        db_table = 'daily_task'

    title = models.CharField(max_length=100)
    time_created = models.DateTimeField(auto_now_add=True)
    due_to = models.DateTimeField()
    has_finished = models.BooleanField(default=False)
    daily_user = models.ForeignKey('DailyUser', related_name='task', on_delete=models.CASCADE)


    def __str__(self, ):
        return self.title

class DailyUser(models.Model):
    class Meta:
        db_table = 'daily_user'

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(choices=gender_choices, max_length=3, default='M') 
    email = models.EmailField(unique=True)
    description = models.TextField(null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self, ):
        return f'{self.first_name} {self.last_name} {self.email}'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.username = self.generate_username()
        super(DailyUser, self).save(*args, **kwargs)


    def generate_username(self, ):
        username = ""
        i = 0
        while DailyUser.objects.filter(username=username).exists() or i == 0:
            username = self.first_name[0] + '.' + self.last_name
            if i:
                username += str(i)
            i += 1
        return username

