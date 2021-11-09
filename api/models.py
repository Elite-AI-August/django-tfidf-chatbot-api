from django.db import models

# Create your models here.
class Question(models.Model):
    query = models.CharField(max_length=50)