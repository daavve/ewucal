# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-19 08:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calligraphy', '0014_auto_20160718_0020'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='image_length_httpRequest',
        ),
        migrations.RemoveField(
            model_name='page',
            name='image_width_httpRequest',
        ),
    ]