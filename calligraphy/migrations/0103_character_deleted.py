# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-16 12:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calligraphy', '0102_auto_20170406_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
