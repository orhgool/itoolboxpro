# Generated by Django 2.1.5 on 2019-04-08 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('halcon', '0003_auto_20190307_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dlfromwebs',
            name='url_text',
            field=models.URLField(max_length=300),
        ),
    ]
