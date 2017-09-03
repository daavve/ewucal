# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-03 00:12
#
# Builds a list of pages that have boxes
#
#######################################################
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


def do_stuff(apps, schemd_editor) -> None:
    Page = apps.get_model('calligraphy', 'Page')
    Char = apps.get_model('calligraphy', 'Character')
    PagesHaveChars = apps.get_model('calligraphy', 'PagesHaveChars')
    for page in Page.objects.all():
        if len(Char.objects.filter(parent_page=page)) > 0:
            PagesHaveChars(haveChars = page).save()


class Migration(migrations.Migration):

    dependencies = [
        ('calligraphy', '0105_auto_20170616_1223'),
    ]

    operations = [
        migrations.CreateModel(
            name='PagesHaveChars',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('haveChars', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calligraphy.Page')),
            ],
        ),
        migrations.RunPython(do_stuff)
    ]
