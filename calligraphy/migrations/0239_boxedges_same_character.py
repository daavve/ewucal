# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-24 22:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calligraphy', '0238_auto_20171116_0649'),
    ]

    operations = [
        migrations.AddField(
            model_name='boxedges',
            name='same_character',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]