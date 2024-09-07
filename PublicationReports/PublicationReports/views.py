import io
import json
import django
from django.core.exceptions import ObjectDoesNotExist

django.setup()
from .models import Author as AuthorModel, Publication as PublModel, Journal as JournalModel
from .forms import AuthorForm, PublicationForm, JournalForm
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
            new_author = AuthorModel(name=author_form.cleaned_data['name'],
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
        author_model = AuthorModel.objects.get(id=id)
    except author_model.DoesNotExist:
        return HttpResponseNotFound('Не найдено')
    if request.method == 'GET':
        author_form = AuthorForm(instance=author_model)
        return TemplateResponse(request,
                                template_name,
                                context={'form': author_form,
                                         'publications': PublModel.objects.filter(author=id)})
    elif request.method == 'POST':
        author_form = AuthorForm(request.POST, request.FILES, instance=author_model)
        if author_form.is_valid():
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
        author_model = AuthorModel.objects.get(id=id)

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

    # считываем файлик json
    with io.open(f'PublicationReports/parse_app/publications_list.json',
                 'r+',
                 encoding='utf-8') as JSON:
        publ_dict = json.load(JSON)

    journal_model = JournalModel()
    publ_model = PublModel()

    for p in publ_dict:
        if p.get('Журнал') is not None:  # если поле журнал не пусто в json файле
            if JournalModel.objects.filter(name=p.get('Журнал'), publisher=p.get(
                    'Издатель')).exists():  # если в базе уже есть такая запись
                pass  # то ниче не делаем
            else:  # если в базе такой записи нет
                if JournalModel.objects.exists():  # журналы - если есть записи, то берем последний номер ид и прибавляем единицу
                    journal_model.id = JournalModel.objects.last().id + 1
                else:  # если записей в таблице нет (т. е. ид пусто) то просто берем единицу
                    journal_model.id = 1
                if PublModel.objects.exists():  # публикации - если есть записи, то берем последний номер ид и прибавляем единицу
                    publ_model.id = PublModel.objects.last().id + 1
                else:  # если записей в таблице нет (т. е. ид пусто) то просто берем единицу
                    publ_model.id = 1
                # задаем журнал
                journal_model.name = p.get('Журнал')
                journal_model.publisher = p.get('Издатель')
                # сохраняем модельки
                journal_model.save(force_insert=True)
                publ_model.save(force_insert=True)
                # добавляем связь многие-ко-многим автор+публикация
                author_model = AuthorModel(id=id)
                publ_model = PublModel(id=id)
                publ_model.author.add(author_model)
                publ_model.save()
                # добавляем данные публикации и связь один-ко-многим с журналом
                journal_model = JournalModel.objects.get(id=journal_model.id)
                p1 = PublModel(id=publ_model.id,
                               title=p.get('Название'),
                               year=p.get('Дата публикации')[0:4],
                               number=p.get('Номер'),
                               volume=p.get('Том'),
                               pages=p.get('Страницы'))
                journal_model.publication_set.add(p1, bulk=False)
                # увеличиваем идентификаторы
                journal_model.id += 1
                publ_model.id += 1

    return HttpResponseRedirect(reverse('index'))
