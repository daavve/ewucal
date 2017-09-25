# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-20 01:00
#
# Normalizes orientation
#
#############################################################


from __future__ import unicode_literals

from django.db import migrations, connection

def do_stuff(apps, schemd_editor) -> None:
    with connection.cursor() as cursor:
        cursor.execute("UPDATE calligraphy_detectedbox SET orientation_norm = CAST( orientation * 683565275 AS int )")

class Migration(migrations.Migration):

    dependencies = [
        ('calligraphy', '0150_detectedbox_orientation_norm'),
    ]

    operations = [ migrations.RunPython(do_stuff)
    ]
