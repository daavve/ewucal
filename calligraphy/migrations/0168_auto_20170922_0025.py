# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-22 00:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calligraphy', '0167_auto_20170920_2147'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detectedbox',
            name='major_axis_length',
        ),
        migrations.RemoveField(
            model_name='detectedbox',
            name='minor_axis_length',
        ),
    ]
