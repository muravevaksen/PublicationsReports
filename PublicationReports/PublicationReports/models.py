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
    name = models.CharField(max_length=200, unique=True, verbose_name='Наименование кафедры')

    def __str__(self):
        return self.name

class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name='ФИО')
    job = models.CharField(max_length=200, verbose_name='Место работы')
    departament = models.ForeignKey(Departament, verbose_name='Кафедра', on_delete=models.CASCADE)
    url = models.CharField(max_length=200, verbose_name='URL Google Scholar')

    def __str__(self):
        return f'{self.name} ({self.departament})'

    class Meta:
        ordering = ['name', 'job', 'departament']
        permissions = (("can_add_teacher", "add teacher"), ("can_update_teacher", "update teacher"),)

class TypeOfPublication(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

class Publication(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, verbose_name='Название')
    year = models.IntegerField(null=True, verbose_name='Год')
    number = models.CharField(max_length=20, null=True, verbose_name='Номер')
    volume = models.CharField(max_length=20, null=True, default=None, blank=True, verbose_name='Том')
    pages = models.CharField(max_length=20, null=True, verbose_name='Страницы')
    citation = models.IntegerField(null=True, verbose_name='Цитирования')
    author = models.ManyToManyField(Author, verbose_name='Автор')
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE, null=True, verbose_name='Журнал')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, verbose_name='Книга')
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, null=True, verbose_name='Конференция')
    type = models.ForeignKey(TypeOfPublication, on_delete=models.CASCADE, default=4, verbose_name='Тип')

    class Meta:
        ordering = ['-year', 'journal', 'number']
        permissions = (("can_add_publication", "add publication"), ("can_update_publication", "update publication"),)
