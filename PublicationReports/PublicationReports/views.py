from .models import Author as AuthorModel, Publication as PublModel
from .forms import AuthorForm, PublicationForm
from django.template.response import TemplateResponse
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseNotFound
from scrapy.crawler import CrawlerProcess
from .parse_app.parse_app.spiders.publ_parse_spider import PublParseSpiderSpider

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
        author_model = AuthorModel.objects.get(pk=id)
    except author_model.DoesNotExist:
        return HttpResponseNotFound('Не найдено')
    if request.method == 'GET':
        author_form = AuthorForm(instance=author_model)
        return TemplateResponse(request,
                                template_name,
                                context={'form': author_form,
                                         'publications': PublModel.objects.all()})
    elif request.method == 'POST':
        author_form = AuthorForm(request.POST, request.FILES, instance=author_model)
        if author_form.is_valid():
            author_form.id = request.POST['id']
            author_form.name = author_form.cleaned_data['name']
            author_form.job = author_form.cleaned_data['job']
            author_form.departament = author_form.cleaned_data['departament']
            author_form.url = author_form.cleaned_data['url']
            author_form.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return TemplateResponse(request,
                                    template_name,
                                    context={'form': author_form})

def update_publications(request, id=None):
    if request.method == 'GET':
        process = CrawlerProcess({'FEED_FORMAT': 'json',
                                  'FEED_URI': 'publications_list.json',
                                  'FEED_EXPORT_ENCODING': 'utf-8'})
        process.crawl(PublParseSpiderSpider, domain="https://scholar.google.com/citations?user=9c_OePYAAAAJ&hl=ru&oi=ao")
        process.start()
        return HttpResponseRedirect(reverse('index'))