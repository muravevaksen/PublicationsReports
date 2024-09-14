import io
import json
import django
from django.db.models import Count

django.setup()
from .models import Author as AuthorModel, Publication as PublModel, Journal as JournalModel
from .forms import AuthorForm, PublicationForm, JournalForm, DepartForm
from django.template.response import TemplateResponse
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseNotFound
from .parse_app.parse_app.spiders.publ_parse_spider import PublParseSpiderSpider
import scrapy.crawler as crawler
import multiprocess as mp
from twisted.internet import reactor


def index(request):
    author_model = AuthorModel.objects.all()
    # считаем количество публикаций каждого автора
    publ_count = AuthorModel.objects.annotate(num_publ=Count("publication"))
    # подготавливаем данные для вывода
    id_author = [x.id for x in author_model]
    name = [x.name for x in author_model]
    depart = [x.departament for x in author_model]
    pcount = [str(x.num_publ) for x in publ_count]
    pcount.reverse()  # обратная сортировочка
    return TemplateResponse(request,
                            'PublicationReports/index.html',
                            context={'authors': author_model,
                                     'id_author': id_author,
                                     'name': name,
                                     'depart': depart,
                                     'pcount': pcount})


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


def view_author(request, author_id):
    template_name = "PublicationReports/author.html"
    try:
        author_model = AuthorModel.objects.get(id=author_id)
    except author_model.DoesNotExist:
        return HttpResponseNotFound('Не найдено')
    if request.method == 'GET':
        author_form = AuthorForm(instance=author_model)
        return TemplateResponse(request,
                                template_name,
                                context={'form': author_form,
                                         'publications': PublModel.objects.filter(author=author_id),
                                         'author_id': author_id})
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


def update_publications(request, author_id):
    try:
        author_model = AuthorModel.objects.get(id=author_id)
    except author_model.DoesNotExist:
        return HttpResponseNotFound('Не найдено')

    if request.method == 'GET':
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
        # *----------------- Обновление данных------------------------------*
        # если в базе уже есть такая запись журнала (полная сверка)
        if JournalModel.objects.filter(name=p.get('Журнал'),
                                       publisher=p.get('Издатель')).exists():
            # если в базе уже есть такая запись публикации (полная сверка)
            if PublModel.objects.filter(title=str(p.get('Название')).capitalize(),
                                        year=p.get('Дата публикации')[0:4],
                                        number=p.get('Номер'),
                                        volume=p.get('Том'),
                                        pages=p.get('Страницы'),
                                        citation=p.get('Цитирования'),
                                        author=AuthorModel.objects.get(id=author_model.id)).exists():
                pass  # ничего не обновляем (повтор)
            # если в базе уже есть такая запись публикации (но не совпадает с автором)
            elif PublModel.objects.filter(title=str(p.get('Название')).capitalize(),
                                          year=p.get('Дата публикации')[0:4],
                                          number=p.get('Номер'),
                                          volume=p.get('Том'),
                                          pages=p.get('Страницы'),
                                          citation=p.get('Цитирования')).exists():
                # то добавляем связь текущего автора и публикации
                author_model = AuthorModel.objects.get(id=author_id)
                author_model.save()
                p1 = PublModel.objects.filter(title=str(p.get('Название')).capitalize(),
                                              year=p.get('Дата публикации')[0:4],
                                              number=p.get('Номер'),
                                              volume=p.get('Том'),
                                              pages=p.get('Страницы'),
                                              citation=p.get('Цитирования'))
                publ_model = PublModel.objects.get(id=p1[0].id)
                publ_model.author.add(author_model)
                publ_model.save()
            else:  # если журнал есть, а публикации нет
                # добавляем связь многие-ко-многим автор+публикация
                publ_model.save(force_insert=True)
                author_model = AuthorModel(id=author_id)
                publ_model = PublModel(id=publ_model.id)
                publ_model.author.add(author_model)
                publ_model.save()
                # добавляем данные публикации и связь один-ко-многим с журналом
                j1 = JournalModel.objects.filter(name=p.get('Журнал'),
                                                 publisher=p.get('Издатель'))
                journal_model = JournalModel.objects.get(id=j1[0].id)
                p1 = PublModel(id=publ_model.id,
                               title=str(p.get('Название')).capitalize(),
                               year=p.get('Дата публикации')[0:4],
                               number=p.get('Номер'),
                               volume=p.get('Том'),
                               pages=p.get('Страницы'),
                               citation=p.get('Цитирования'))
                journal_model.publication_set.add(p1, bulk=False)
                publ_model.id += 1
        # *----------------- Новые записи ------------------------------*
        else:
            if JournalModel.objects.exists():  # журналы - если есть записи, то берем последний номер ид и прибавляем единицу
                journal_model.id = JournalModel.objects.last().id + 1
            else:  # Если записей в таблице нет (т. е. ид пусто), то просто берем единицу
                journal_model.id = 1
            if PublModel.objects.exists():  # публикации - если есть записи, то берем последний номер ид и прибавляем единицу
                publ_model.id = PublModel.objects.last().id + 1
            else:  # Если записей в таблице нет (т. е. ид пусто), то просто берем единицу
                publ_model.id = 1
            # задаем журнал
            journal_model.name = p.get('Журнал')
            journal_model.publisher = p.get('Издатель')
            # сохраняем модельки
            journal_model.save(force_insert=True)
            publ_model.save(force_insert=True)
            # добавляем связь многие-ко-многим автор+публикация
            author_model = AuthorModel(id=author_id)
            publ_model = PublModel(id=publ_model.id)
            publ_model.author.add(author_model)
            publ_model.save()
            # добавляем данные публикации и связь один-ко-многим с журналом
            journal_model = JournalModel.objects.get(id=journal_model.id)
            p1 = PublModel(id=publ_model.id,
                           title=str(p.get('Название')).capitalize(),
                           year=p.get('Дата публикации')[0:4],
                           number=p.get('Номер'),
                           volume=p.get('Том'),
                           pages=p.get('Страницы'),
                           citation=p.get('Цитирования'))
            journal_model.publication_set.add(p1, bulk=False)
            # увеличиваем идентификаторы
            journal_model.id += 1
            publ_model.id += 1

    return HttpResponseRedirect(reverse('index'))


def export_to_excel(request, author_id):
    return HttpResponseRedirect(reverse('index'))

# это надо переписать
def edit_publications(request, author_id, publ_id):
    template_name = "PublicationReports/edit_publications.html"
    try:
        author_model = AuthorModel.objects.get(id=author_id)
    except author_model.DoesNotExist:
        return HttpResponseNotFound('Не найдено')
    if request.method == 'GET':
        author_form = AuthorForm(instance=author_model)
        return TemplateResponse(request,
                                template_name,
                                context={'form': author_form,
                                         'publications': PublModel.objects.filter(author=author_id),
                                         'author_id': author_id})
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

def departaments(request):
    template_name = "PublicationReports/departaments.html"
    return TemplateResponse(request,
                            template_name,
                            context={'form': DepartForm})
