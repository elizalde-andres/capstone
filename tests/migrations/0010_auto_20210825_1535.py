# Generated by Django 3.2.5 on 2021-08-25 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0009_alter_testpart_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=128),
        ),
    ]