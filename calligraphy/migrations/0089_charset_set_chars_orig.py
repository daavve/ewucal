# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-22 18:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calligraphy', '0088_auto_20170322_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='charset',
            name='set_chars_orig',
            field=models.ManyToManyField(to='calligraphy.Character_orig'),
        ),
    ]
