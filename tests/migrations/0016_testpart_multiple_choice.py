# Generated by Django 3.2.5 on 2021-08-26 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0015_test_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='testpart',
            name='multiple_choice',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
