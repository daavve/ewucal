# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-19 23:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calligraphy', '0140_auto_20170919_2337'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detectedbox',
            name='convex_area',
        ),
    ]