# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-26 04:02
# Fills out page database with images on hard drive
#
######################################################


from __future__ import unicode_literals

from django.db import migrations
import socket
import os

HOSTNAME = socket.gethostname()
if HOSTNAME == 'bigArch':
    IMAGE_DIR = "/home/dave/workspace/pycharm/media/pages/"
else:
    IMAGE_DIR = "/media/media/pages/"


def add_pages_from_filesystem(apps) -> None:
    Page = apps.get_model("calligraphy", "Page")
    for f in os.listdir(IMAGE_DIR):
        if f.endswith('.jpg'):
            pathname = os.path.join(IMAGE_DIR, f)
            bkpg = f.strip('.jpg').split('-')
            bk = int(bkpg[0])
            pg = int(bkpg[1])
            page = Page.objects.filter(page_bookid=bk).filter(page_pageid=pg)
            if len(page) == 0:
                pg = Page(page_image=pathname, page_bookid=bk, page_pageid=pg)
                pg.save()
        else:
            if f.endswith('.png') and not f.endswith('s.png'):  # Skip the small image version
                pathname = os.path.join(IMAGE_DIR, f)
                bkpg = f.strip('.png').split('-')
                bk = int(bkpg[0])
                pg = int(bkpg[1])
                page = Page.objects.filter(page_bookid=bk, page_pageid=pg)
                if len(page) == 0:
                    pg = Page(page_image=pathname, page_bookid=bk, page_pageid=pg)
                    pg.save()
            else:
                if f.endswith('.tif'):
                    pathname = os.path.join(IMAGE_DIR, f)
                    bkpg = f.strip('.tif').split('-')
                    bk = int(bkpg[0])
                    pg = int(bkpg[1])
                    page = Page.objects.filter(page_bookid=bk, page_pageid=pg)
                    if len(page) == 0:
                        pg = Page(page_image=pathname, page_bookid=bk, page_pageid=pg)
                        pg.save()



def import_data(apps, schemd_editor) -> None:
    add_pages_from_filesystem(apps)

class Migration(migrations.Migration):

    dependencies = [
        ('calligraphy', '0002_auto_20160225_1957'),
    ]

    operations = [ migrations.RunPython(import_data)
    ]
