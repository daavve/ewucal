# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-26 22:30
#
# This one removes fields are currently aren't using
#
###############################################################
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calligraphy', '0005_auto_20160225_2207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='character',
            name='char_author',
        ),
        migrations.RemoveField(
            model_name='character',
            name='char_mark',
        ),
    ]
