"""
URL configuration for PublicationReports project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import index, create_teacher, view_author, update_publications, export_to_excel, edit_publications, departaments
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('create_teacher/', create_teacher, name="create_teacher"),
    path('', index, name="index"),
    path('author/<int:author_id>/', view_author, name="view_author"),
    path('author/<int:author_id>/update/', update_publications, name="update_publications"),
    path('author/<int:author_id>/export/', export_to_excel, name="export_to_excel"),
    path('author/<int:author_id>/edit/<int:publ_id>', edit_publications, name="edit_publications"),
    path('departaments', departaments, name="departaments"),
]
