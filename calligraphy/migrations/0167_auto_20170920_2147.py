# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-20 21:47
from __future__ import unicode_literals

from django.db import migrations
import numpy as np

def do_stuff(apps, schemd_editor) -> None:
    Char_ori = apps.get_model('calligraphy', 'Character_orig').objects
    Pages = apps.get_model('calligraphy', 'Page').objects
    DetectedBox = apps.get_model('calligraphy', 'DetectedBox').objects
    PagesHaveChars = apps.get_model('calligraphy', 'PagesHaveChars').objects
    for thisPage in PagesHaveChars.all():
        curPage = Pages.get(id=thisPage.haveChars.id)
        chars_ori = Char_ori.filter(parent_page=curPage)
        features  = DetectedBox.filter(parent_page=curPage)
        print("ID: " + str(thisPage.haveChars.id) + " Chars: " + str(len(chars_ori)) + " Features: " + str(len(features)))
        grid_val = np.zeros([curPage.image_length,curPage.image_width], dtype=np.uint8)
        for char_orig in chars_ori:
            grid_val[char_orig.y1:char_orig.y2, char_orig.x1:char_orig.x2].fill(1)
        for feature in features:
            sum_ori = np.sum(grid_val[feature.y1:feature.y2, feature.x1:feature.x2])
            area = (feature.y2 - feature.y1) * (feature.x2 - feature.x1)
            area_percent = int(100 * sum_ori / area)
            if area_percent >= 80:
                feature.inside_orig_box = True
            else:
                feature.inside_orig_box = False
            feature.save(update_fields=['inside_orig_box'])

class Migration(migrations.Migration):

    dependencies = [
        ('calligraphy', '0166_auto_20170920_0250'),
    ]

    operations = [ migrations.RunPython(do_stuff)
    ]
