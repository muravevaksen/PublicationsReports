# Generated by Django 4.2.15 on 2024-09-06 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PublicationReports', '0012_rename_id_journal_publication_journal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publication',
            name='citation',
        ),
    ]
