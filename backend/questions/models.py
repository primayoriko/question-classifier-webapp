from django.db import models

# Create your models here.
Topics = ('A', 'B', 'C')

class Question(models.Model):
    question_text = models.CharField(max_length=500)
    topic = models.CharField(max_length=25)