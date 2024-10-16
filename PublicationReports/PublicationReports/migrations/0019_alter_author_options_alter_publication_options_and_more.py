# Generated by Django 4.2.15 on 2024-10-18 08:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PublicationReports', '0018_alter_publication_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['name', 'job', 'departament'], 'permissions': (('can_add_teacher', 'add teacher'), ('can_update_teacher', 'update teacher'))},
        ),
        migrations.AlterModelOptions(
            name='publication',
            options={'ordering': ['-year', 'journal', 'number'], 'permissions': (('can_add_publication', 'add publication'), ('can_update_publication', 'update publication'))},
        ),
        migrations.AlterField(
            model_name='author',
            name='departament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PublicationReports.departament', verbose_name='Кафедра'),
        ),
        migrations.AlterField(
            model_name='author',
            name='job',
            field=models.CharField(max_length=200, verbose_name='Место работы'),
        ),
        migrations.AlterField(
            model_name='author',
            name='name',
            field=models.CharField(max_length=200, verbose_name='ФИО'),
        ),
        migrations.AlterField(
            model_name='author',
            name='url',
            field=models.CharField(max_length=200, verbose_name='URL Google Scholar'),
        ),
        migrations.AlterField(
            model_name='departament',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Наименование кафедры'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='author',
            field=models.ManyToManyField(to='PublicationReports.author', verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='PublicationReports.book', verbose_name='Книга'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='citation',
            field=models.IntegerField(null=True, verbose_name='Цитирования'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='conference',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='PublicationReports.conference', verbose_name='Конференция'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='journal',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='PublicationReports.journal', verbose_name='Журнал'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='number',
            field=models.CharField(max_length=20, null=True, verbose_name='Номер'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='pages',
            field=models.CharField(max_length=20, null=True, verbose_name='Страницы'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='type',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, to='PublicationReports.typeofpublication', verbose_name='Тип'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='volume',
            field=models.CharField(default=None, max_length=20, null=True, verbose_name='Том'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='year',
            field=models.IntegerField(null=True, verbose_name='Год'),
        ),
    ]
