# Generated by Django 3.2.5 on 2021-08-26 20:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0018_rename_content_testpart_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testpart',
            old_name='title',
            new_name='content',
        ),
    ]
