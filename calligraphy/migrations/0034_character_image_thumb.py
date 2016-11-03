# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-18 02:59
#
# Just creates thumbnails so we can do the website while the migration is onging
#
#########################################################################################################
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models
from PIL import Image
from PIL.ImageChops import difference
from PIL.ImageOps import autocontrast
from ..models import Page, Character

class Migration(migrations.Migration):

    dependencies = [
        ('calligraphy', '0033_auto_20161017_1959'),
    ]

    operations = [
            migrations.AddField(
            model_name='character',
            name='image_thumb',
            field=models.ImageField(blank=True, storage=django.core.files.storage.FileSystemStorage(), upload_to=''),
        ),
            migrations.CreateModel(
            name='PageMultiplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_score', models.IntegerField()),
                ('x_mult', models.FloatField()),
                ('y_mult', models.FloatField()),
                ('parent_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calligraphy.Page')),
            ])
    ]
