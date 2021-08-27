# Generated by Django 3.2.5 on 2021-08-27 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0027_auto_20210827_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testassignment',
            name='finished_date',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='testassignment',
            name='score',
            field=models.DecimalField(blank=True, decimal_places=1, default=None, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='testassignment',
            name='score_percent',
            field=models.DecimalField(blank=True, decimal_places=1, default=None, max_digits=4, null=True),
        ),
    ]
