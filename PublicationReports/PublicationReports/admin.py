from django.contrib import admin
from .models import Publication, Author

class PiblicationsAdmin(admin.ModelAdmin):
    list_display = ('ID', 'Title', 'Year', 'Number', 'Volume', 'Citation', 'Pages', 'ID_Journal')

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('ID', 'Name', 'Job', 'Departament', 'URL')

admin.site.register(Publication)
admin.site.register(Author)