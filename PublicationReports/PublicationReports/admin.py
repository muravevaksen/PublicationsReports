from django.contrib import admin
from .models import Publication

class PiblicationsAdmin(admin.ModelAdmin):
    list_display = ('ID', 'Title', 'Year', 'Number', 'Volume', 'Citation', 'Pages', 'ID_Journal')

admin.site.register(Publication)