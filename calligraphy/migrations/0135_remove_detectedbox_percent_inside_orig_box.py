# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-19 14:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calligraphy', '0134_auto_20170919_0012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detectedbox',
            name='percent_inside_orig_box',
        ),
    ]
