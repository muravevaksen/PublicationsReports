from django.db import models

class Journal(models.Model):
    id = models.IntegerField(max_length=8, primary_key=True)
    name = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)

class Publication(models.Model):
    id = models.IntegerField(max_length=8, primary_key=True)
    title = models.CharField(max_length=200)
    year = models.IntegerField(max_length=4)
    number = models.CharField(max_length=20)
    volume = models.CharField(max_length=20)
    citation = models.CharField(max_length=20)
    pages = models.CharField(max_length=20)
    id_journal = models.ForeignKey(Journal, on_delete=models.CASCADE)

class Departament(models.Model):
    id = models.IntegerField(max_length=8, primary_key=True)
    name = models.CharField(max_length=200)

class Author(models.Model):
    id = models.IntegerField(max_length=8, primary_key=True)
    name = models.CharField(max_length=200)
    job = models.CharField(max_length=200)
    departament = models.ForeignKey(Departament, on_delete=models.CASCADE)
    url = models.CharField(max_length=200)

    class Meta:
        permissions = (("can_add_teacher", "add teacher"), ("can_update_teacher", "update teacher"),)

class AuthorOfPublication(models.Model):
    id = models.IntegerField(max_length=8, primary_key=True)
    id_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    id_publication = models.ForeignKey(Publication, on_delete=models.CASCADE)

