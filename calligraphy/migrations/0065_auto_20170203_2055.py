# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-03 20:55
#
# This flattens the character directory hierarchy so we can
# more cleanly deal with our chars at Amazon S3.
#
###############################################################
from __future__ import unicode_literals

from django.db import migrations

def flatten_dir(apps) -> None:
    Chars = apps.get_model('calligraphy', 'Character')
    for char in Chars.objects.all():
        char_split = char.image.path.split('/')
        char_new = '/media/chars' + char_split[3] + '-' + char_split[4]
        char.path = char_new
        char.save()
        


def do_stuff(apps, schemd_editor) -> None:
    flatten_dir(apps)

class Migration(migrations.Migration):

    dependencies = [
        ('calligraphy', '0064_auto_20170131_1511'),
    ]

    operations = [ migrations.RunPython(do_stuff)
    ]
