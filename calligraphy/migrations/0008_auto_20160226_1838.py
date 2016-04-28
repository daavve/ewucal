# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-27 01:31
#
# Loads scanned images json into database
#
####################################################
from __future__ import unicode_literals

from django.db import migrations
import socket
import json
import os

if socket.gethostname() == 'bigArch':
    MEDIA_DIR = "/home/dave/workspace/pycharm/media/"
else:
    MEDIA_DIR = "/media/media/"

def readjson(apps) -> None:
    Author = apps.get_model("calligraphy", "Author")
    Work = apps.get_model("calligraphy", "Work")
    Page = apps.get_model("calligraphy", "Page")
    jsonfile = open("c-scannedwork-1.json", mode="r", encoding='utf-8')
    r = json.load(jsonfile)
    jsonfile.close()
#    for r in readfile:
    auth = r['author']
    author = Author.objects.filter(author_name=auth)[0]
    title =  r['title']
    wkid = int(r['wkid'])
    work = Work(work_id=wkid, work_title=title, work_author=author)
    work.save()
    for p in r['pages']:
        filepath = MEDIA_DIR + p['filepath']
        if not os.path.isfile(filepath):
            Exception("Image not found")
        transcpt = p['transcript']
        page = Page(page_image=filepath, page_transcript=transcpt, parent_work=work)
        page.save()


def import_data(apps, schemd_editor) -> None:
    readjson(apps)

class Migration(migrations.Migration):

    dependencies = [
        ('calligraphy', '0007_auto_20160226_1731'),
    ]

    operations = [ migrations.RunPython(import_data)
    ]
