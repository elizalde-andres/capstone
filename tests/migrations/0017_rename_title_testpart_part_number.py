# Generated by Django 3.2.5 on 2021-08-26 20:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0016_testpart_multiple_choice'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testpart',
            old_name='title',
            new_name='part_number',
        ),
    ]