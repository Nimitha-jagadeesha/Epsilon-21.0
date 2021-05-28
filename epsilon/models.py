from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from django.contrib.postgres.fields import ArrayField
# Create your models here.
class Question(models.Model):
    number = models.IntegerField(default=0)
    question = models.TextField()
    answer = models.TextField()
    date_created = models.DateTimeField(default = timezone.now)
    image = models.TextField(default='none.jpg')

    def __str__(self):
        return str(self.number)

class Score(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    question_number = models.IntegerField(default=1)
    last_submit = models.DateTimeField(default=timezone.now)
    visible = models.BooleanField(default=True)
    picked = ArrayField(models.IntegerField())

    def __str__(self):
        return f'{self.user.username} ({self.last_submit})'