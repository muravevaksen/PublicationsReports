from django.db import models

class Journal(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True, null=True)
    publisher = models.CharField(max_length=200, null=True)

class Book(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True, null=True)
    publisher = models.CharField(max_length=200, null=True)

class Conference(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True, null=True)

class Departament(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)

class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name='ФИО')
    job = models.CharField(max_length=200, verbose_name='Место работы')
    departament = models.ForeignKey(Departament, verbose_name='Кафедра', on_delete=models.CASCADE)
    url = models.CharField(max_length=200, verbose_name='URL Google Scholar')

    class Meta:
        permissions = (("can_add_teacher", "add teacher"), ("can_update_teacher", "update teacher"),)

class TypeOfPublication(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

class Publication(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    year = models.IntegerField(null=True)
    number = models.CharField(max_length=20, null=True)
    volume = models.CharField(max_length=20, null=True)
    pages = models.CharField(max_length=20, null=True)
    citation = models.IntegerField(null=True)
    author = models.ManyToManyField(Author)
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, null=True)
    type = models.ForeignKey(TypeOfPublication, on_delete=models.CASCADE, default=4)

    class Meta:
        ordering = ['-year', 'journal', 'number']
