from django.db import models

Topics = ('BUSINESS', 
    'ENTERTAINMENT', 
    'HEALTH', 
    'NATION', 
    'SCIENCE', 
    'SPORTS',
    'TECHNOLOGY',
    'WORLD')

class Question(models.Model):
    question_text = models.CharField(max_length=500)
    topic = models.CharField(max_length=25)

    @classmethod
    def create_instance(cls, topic, text):
        question = cls(topic=topic, question_text=text)
        return question
