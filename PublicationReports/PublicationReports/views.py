import django.http
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .models import Publication as PublModel
from .models import Author as AuthorModel
from .forms import PublicationForm
from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.db import models
from django.views.decorators.http import require_GET, require_http_methods

def index(request):
    return TemplateResponse(request, 'PublicationReports/index.html', context={'authors': AuthorModel.objects.all()})