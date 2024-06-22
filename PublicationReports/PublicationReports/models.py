from django.db import models

class Publications(models.Model):
    id = models.IntegerField(max_length=5, primary_key=True)
    title = models.CharField(max_length=1000)
    year = models.IntegerField(max_length=4)
    number = models.CharField(max_length=50)
    volume = models.CharField(max_length=50)
    citation = models.CharField(max_length=50)
    pages = models.CharField(max_length=10)
    id_journal = models.CharField(max_length=10)

class Journals(models.Model):
        id = models.IntegerField(max_length=5, primary_key=True)
        name = models.CharField(max_length=1000)
        publisher = models.CharField(max_length=500)

class Authors(models.Model):
    id = models.IntegerField(max_length=5, primary_key=True)
    name = models.CharField(max_length=100)
    job = models.CharField(max_length=100)
    departament = models.CharField(max_length=200)
    url = models.CharField(max_length=500)

class Departaments(models.Model):
    id = models.IntegerField(max_length=5, primary_key=True)
    name = models.CharField(max_length=200)
