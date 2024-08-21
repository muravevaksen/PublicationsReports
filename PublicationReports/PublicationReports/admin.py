from django.contrib import admin
from .models import Publication

class PiblicationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'year', 'number', 'volume', 'citation', 'pages', 'id_journal')

admin.site.register(Publication)