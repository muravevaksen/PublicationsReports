from django.views.decorators.http import require_http_methods

from .models import Author as AuthorModel
from .forms import AuthorForm
from django.template.response import TemplateResponse
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseNotFound


def index(request):
    return TemplateResponse(request,
                            'PublicationReports/index.html',
                            context={'authors': AuthorModel.objects.all()})

def create_teacher(request):
    template_name = "PublicationReports/new_teacher.html"
    if request.method == 'GET':
        author_form = AuthorForm()
        return TemplateResponse(request,
                                template_name,
                                context={'form': author_form})
    elif request.method == 'POST':
        author_form = AuthorForm(request.POST, request.FILES)
        if author_form.is_valid():
            new_author = AuthorModel(id=author_form.cleaned_data['id'],
                                    name=author_form.cleaned_data['name'],
                                    job=author_form.cleaned_data['job'],
                                    departament=author_form.cleaned_data['departament'],
                                    url=author_form.cleaned_data['url'])
            new_author.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return TemplateResponse(request,
                                    template_name,
                                    context={'form': author_form})

def view_author(request, id):
    template_name = "PublicationReports/author.html"
    try:
        publrep = AuthorModel.objects.get(pk=id)
    except AuthorModel.DoesNotExist:
        return HttpResponseNotFound('Не найдено')
    if request.method == 'GET':
        publrep_form = AuthorForm(instance=publrep)
        return TemplateResponse(request,
                                template_name,
                                context={'form': publrep_form})
    elif request.method == 'POST':
        publrep_form = AuthorForm(request.POST, request.FILES, instance=publrep)
        if publrep_form.is_valid():
            publrep.name = request.POST['name']
            publrep.description = publrep_form.cleaned_data['description']
            publrep.cost = publrep_form.cleaned_data['cost']
            publrep.curr = publrep_form.cleaned_data['curr']
            publrep.rubric = publrep_form.cleaned_data['rubric']
            publrep.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return TemplateResponse(request,
                                    template_name,
                                    context={'form': publrep_form})