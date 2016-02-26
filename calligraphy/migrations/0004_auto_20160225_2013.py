# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-26 04:13
#
# Populates Chars database from chars file
#
######################################################
from __future__ import unicode_literals

from django.db import migrations
import json
import socket
import os

if socket.gethostname() == 'bigArch':
    CHARS_DIR = "/home/dave/workspace/pycharm/fetch/chars"
else:
    CHARS_DIR = "/media/chars/"

def addchars(apps) -> None:
    Page = apps.get_model("calligraphy", "Page")
    Char = apps.get_model("calligraphy", "Character")
    jsonfile = open("c-chars.json", mode="r", encoding='utf-8')
    readfile = json.load(jsonfile)
    jsonfile.close()
    for r in readfile:
        mark = r['chi_mark']
        bkid = r['work_id']
        pgid = r['page_id']
        cord = r['xy_coordinates']
        x1 = cord[0]
        y1 = cord[1]
        x2 = cord[2]
        y2 = cord[3]
        pfile = bkid + '/' + pgid + '(' + x1 + ',' + y1 + ',' + x2 + ',' + y2 + ').jpg'
        path = CHARS_DIR + pfile
        if not os.path.isfile(path):
            Exception("file not found: ", path)

        page = Page.objects.filter(page_bookid=int(bkid)).filter(page_pageid=int(pgid))[0]
        char = Char(parent_page=page, char_mark=mark, char_image=path,
                    x1=int(x1), y1=int(y1), x2=int(x2), y2=int(y2))
        char.save()


def import_data(apps, schemd_editor) -> None:
    addchars(apps)

class Migration(migrations.Migration):

    dependencies = [
        ('calligraphy', '0003_auto_20160225_2002'),
    ]

    operations = [ migrations.RunPython(import_data)
    ]
