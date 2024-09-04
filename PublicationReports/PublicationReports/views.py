import io
import json

import django
django.setup()
from .models import Author as AuthorModel, Publication as PublModel
from .forms import AuthorForm, PublicationForm
from django.template.response import TemplateResponse
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseNotFound
from .parse_app.parse_app.spiders.publ_parse_spider import PublParseSpiderSpider
import scrapy.crawler as crawler
import multiprocess as mp
from twisted.internet import reactor

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

def update_publications(request, id):
    if request.method == 'GET':
        author_model = AuthorModel.objects.get(pk=id)
        def f(q):
            try:
                runner = crawler.CrawlerRunner()
                deferred = runner.crawl(PublParseSpiderSpider, domain=author_model.url)
                deferred.addBoth(lambda _: reactor.stop())
                reactor.run()
                q.put(None)
            except Exception as e:
                q.put(e)

        q = mp.Queue()
        p = mp.Process(target=f, args=(q,))
        p.start()
        result = q.get()
        p.join()
        if result is not None:
            raise result

        with io.open(f'PublicationReports/parse_app/publications_list.json',
                     'r+',
                     encoding='utf-8') as JSON:
            publ_dict = json.load(JSON)

        return HttpResponseRedirect(reverse('index'))



