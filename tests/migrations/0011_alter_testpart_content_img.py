# Generated by Django 3.2.5 on 2021-08-25 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0010_auto_20210825_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testpart',
            name='content_img',
            field=models.ImageField(blank=True, upload_to='tests/'),
        ),
    ]
