# Generated by Django 2.1.5 on 2019-04-08 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('halcon', '0004_auto_20190408_0940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dlfromwebs',
            name='url_text',
            field=models.URLField(),
        ),
    ]