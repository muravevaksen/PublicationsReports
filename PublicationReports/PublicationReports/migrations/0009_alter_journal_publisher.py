# Generated by Django 4.2.15 on 2024-09-04 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PublicationReports', '0008_alter_journal_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='publisher',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
