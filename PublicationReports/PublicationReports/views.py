from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView
from .models import Publication as PublicationModel
from .forms import PublicationForm
from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.db import models
def post_list(request):
    posts = PublicationModel.published.all()
    return render(request, 'PublicationReports/index.html', {'posts': posts})

def index(request):
    return TemplateResponse(request,
                            'PublicationReports/index.html',
                            context={"rubrics": 'текст'
                                     }
                            )