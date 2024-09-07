from django.db import models

class Journal(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    publisher = models.CharField(max_length=200, null=True)

class Departament(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)

class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    job = models.CharField(max_length=200)
    departament = models.ForeignKey(Departament, on_delete=models.CASCADE)
    url = models.CharField(max_length=200)

    class Meta:
        permissions = (("can_add_teacher", "add teacher"), ("can_update_teacher", "update teacher"),)

class Publication(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    year = models.IntegerField(max_length=2, null=True)
    number = models.CharField(max_length=20, null=True)
    volume = models.CharField(max_length=20, null=True)
    pages = models.CharField(max_length=20, null=True)
    author = models.ManyToManyField(Author)
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE, null=True)
