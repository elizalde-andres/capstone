# Generated by Django 3.2.5 on 2021-08-26 20:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0020_alter_testpart_part_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testpart',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parts', to='tests.test'),
        ),
    ]
