# -*- coding: utf-8 -*-
#
# This one changes all tiffs in the database to pngs to reflect changes in filesystem
# I did this because firefox has issues rendering some of the tiffs
#
#########################################################
from __future__ import unicode_literals

from django.db import migrations
from django.db import migrations
from django.db import migrations, models


def all_tif_to_png(apps) -> None:
    Character = apps.get_model('calligraphy', 'Character')
    Page = apps.get_model('calligraphy', 'Page')
    chars = Character.objects.all()
    for char in chars:
        imgName = str(char.image_high_rez)
        if 'tif' in imgName:
            char.image_high_rez = imgName.strip('tif') + 'png'
            char.save()
    pages = Page.objects.all()
    for page in pages:
        imgName = str(page.image)
        if 'tif' in imgName:
            page.image = imgName.strip('tif') + 'png'
            page.save()


def do_stuff(apps, schemd_editor) -> None:
    all_tif_to_png(apps)


class Migration(migrations.Migration):

    dependencies = [
        ('calligraphy', '0042_auto_20161115_1210'),
    ]

    operations = [ migrations.RunPython(do_stuff)
    ]
