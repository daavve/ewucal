# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-02 00:47
#
# Found it easier to go through the steps incrementally
#
###########################################################
from __future__ import unicode_literals

from django.db import migrations

import numpy as np


def do_stuff(apps, schemd_editor):
    DetectedCombinedBox = apps.get_model('calligraphy', 'DetectedCombinedBox').objects
    Pages = apps.get_model('calligraphy', 'Page').objects.filter(has_copyright_restrictions=True)
    for curPage in Pages:
        grid = np.zeros((curPage.image_length, curPage.image_width), dtype=np.int)
        box_dict = dict()
        for box in DetectedCombinedBox.filter(parent_page=curPage):
            unique = np.unique(grid[box.y1:box.y2, box.x1:box.x2])
            if len(unique) > 1 or unique[0] != 0:
                overlaps = []
                for unique_i in unique:
                    if unique_i not in overlaps and unique_i != 0:
                        overlaps.append(unique_i)
                for overlap in overlaps:
                    overlap_box = box_dict[overlap]
                    box.y1 = min(box.y1, overlap_box.y1)
                    box.y2 = max(box.y2, overlap_box.y2)
                    box.x1 = min(box.x1, overlap_box.x1)
                    box.x2 = max(box.x2, overlap_box.x2)
                    del box_dict[overlap]
                    overlap_box.delete()
            grid[box.y1:box.y2, box.x1:box.x2].fill(box.id)
            box_dict[box.id] = box
        for box in box_dict:
            box_dict[box].save()


class Migration(migrations.Migration):

    dependencies = [
        ('calligraphy', '0181_auto_20171001_2106'),
    ]

    operations = [ migrations.RunPython(do_stuff)
    ]
