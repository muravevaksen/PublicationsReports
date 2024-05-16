from django.db import models

class Publication(models.Model):
    "Модель публикации"
    id = models.IntegerField(max_length=5)
    author = models.CharField(max_length=50)
    title = models.CharField(max_length=1000)