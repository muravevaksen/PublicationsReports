# Generated by Django 4.2.15 on 2024-08-28 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PublicationReports', '0003_alter_author_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'permissions': (('can_add_teacher', 'add teacher'),)},
        ),
        migrations.AlterField(
            model_name='author',
            name='departament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PublicationReports.departament'),
        ),
        migrations.AlterField(
            model_name='departament',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='publication',
            name='id_journal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PublicationReports.journal'),
        ),
        migrations.CreateModel(
            name='AuthorOfPublication',
            fields=[
                ('id', models.IntegerField(max_length=5, primary_key=True, serialize=False)),
                ('id_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PublicationReports.author')),
                ('id_publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PublicationReports.publication')),
            ],
        ),
    ]
