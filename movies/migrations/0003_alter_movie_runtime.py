# Generated by Django 3.2.8 on 2021-10-24 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_rename_name_genre_genre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='runtime',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
    ]
