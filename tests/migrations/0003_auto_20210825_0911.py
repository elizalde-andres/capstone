# Generated by Django 3.2.5 on 2021-08-25 09:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0002_test_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answer',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='answer',
            name='score',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=4),
        ),
        migrations.AlterField(
            model_name='question',
            name='max_score',
            field=models.DecimalField(decimal_places=1, default=1, max_digits=4),
        ),
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='test',
            name='assigned_students',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='assigned_tests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='test',
            name='finished_students',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='finished_test', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='test',
            name='parts',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='test', to='tests.testpart'),
        ),
        migrations.AlterField(
            model_name='testpart',
            name='content',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='testpart',
            name='content_img',
            field=models.ImageField(blank=True, upload_to='media/tests/'),
        ),
        migrations.AlterField(
            model_name='testpart',
            name='questions',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='test_part', to='tests.question'),
        ),
    ]
