# Generated by Django 3.2.8 on 2021-10-24 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_auto_20211023_2250'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='poster',
            field=models.URLField(blank=True, null=True),
        ),
    ]