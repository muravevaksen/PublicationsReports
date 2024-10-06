from django.contrib import admin
from .models import Publication, Author, Departament, Journal, Book, Conference, TypeOfPublication

class JournalAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'publisher')

class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'publisher')

class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class TypesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class PiblicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'year', 'number', 'volume', 'citation', 'pages', 'id_journal')

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'job', 'departament', 'URL')

class DepartamentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(Journal)
admin.site.register(Book)
admin.site.register(Conference)
admin.site.register(Publication)
admin.site.register(Departament)
admin.site.register(Author)
admin.site.register(TypeOfPublication)