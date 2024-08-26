from .models import Author as AuthorModel
from .forms import AuthorForm
from django.template.response import TemplateResponse
from django.urls import reverse
from django.http import HttpResponseRedirect

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
            new_author = AuthorForm(name=author_form.cleaned_data['name'],
                                   job=author_form.cleaned_data['job'],
                                   departament=author_form.cleaned_data['departament'],
                                   url=author_form.cleaned_data['url'])
            new_author.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return TemplateResponse(request,
                                    template_name,
                                    context={'form': author_form})