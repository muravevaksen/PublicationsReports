from django.db import models

class Publication(models.Model):
    id = models.IntegerField(max_length=5)
    author = models.CharField(max_length=50)
    title = models.CharField(max_length=1000)
    year = models.IntegerField(max_length=4)
    number = models.CharField(max_length=50)
    volume = models.CharField(max_length=50)
    citation = models.CharField(max_length=50)
    journal = models.CharField(max_length=100)
    pages = models.CharField(max_length=10)
    publisher = models.CharField(max_length=100)
