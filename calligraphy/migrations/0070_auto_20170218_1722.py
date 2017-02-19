# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-18 17:22
#
# Fixes page path due to things located differently on new server
# Note:  Had to do it again in the next one due to missing tab
#
#################################################################

from __future__ import unicode_literals

from django.db import migrations

def update_page_path(apps) -> None:
    for page in apps.get_model('calligraphy', 'Page').objects.all():
        page.image = '/static' + str(page.image)
    page.save()

def do_stuff(apps, schemd_editor) -> None:
    update_page_path(apps)


class Migration(migrations.Migration):

    dependencies = [
        ('calligraphy', '0069_auto_20170218_1649'),
    ]

    operations = [ migrations.RunPython(do_stuff)
    ]
