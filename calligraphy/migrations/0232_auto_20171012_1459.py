# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-12 14:59
#
# Goes through and writes 王羲之 related sets to disk
#
######################################################
from __future__ import unicode_literals

from django.db import migrations
import numpy as np

def build_np(boxes):
    features = np.zeros((len(boxes), 10), dtype=np.int32)
    bin_good = np.zeros(len(boxes), dtype=np.bool)
    bin_bad  = np.zeros(len(boxes), dtype=np.bool)
    for i in range(len(boxes)):
        bin_good[i] = boxes[i].inside_currated_box
        bin_bad[i]  = boxes[i].inside_orig_box
        features[i][0] = boxes[i].area_norm
        features[i][1] = boxes[i].eccentricity_norm
        features[i][2] = boxes[i].solidity_norm
        features[i][3] = boxes[i].orientation_norm
        features[i][4] = boxes[i].li_threshold_bottom_norm
        features[i][5] = boxes[i].li_threshold_top_norm
        features[i][6] = boxes[i].local_centroid_x_norm
        features[i][7] = boxes[i].local_centroid_y_norm
        features[i][8] = boxes[i].major_axis_length_norm
        features[i][9] = boxes[i].minor_axis_length_norm
    return features, bin_bad, bin_good

def do_stuff(apps, schemd_editor):
    DetectedBox = apps.get_model('calligraphy', 'DetectedBox').objects
    my_author = apps.get_model('calligraphy', 'Author').objects.get(id=15) # 王羲之
    my_works = apps.get_model('calligraphy', 'Work').objects.filter(author=my_author)
    my_pages_white = apps.get_model('calligraphy', 'Page').objects.filter(has_copyright_restrictions=False, black_chars=False, parent_author=my_author)
    my_pages_all = apps.get_model('calligraphy', 'Page').objects.filter(has_copyright_restrictions=False, parent_author=my_author)
    first_loop = True
    web_ftrs = None
    web_bin_bads = None
    web_bin_goods = None
    for page_web in my_pages_white:
        boxes = DetectedBox.filter(parent_page=page_web)
        if len(boxes) > 0:
            web_ftr, web_bin_bad, web_bin_good = build_np(boxes)
            if first_loop:
                web_ftrs = web_ftr
                web_bin_bads = web_bin_bad
                web_bin_goods = web_bin_good
                first_loop = False
            else:
                web_ftrs = np.append(web_ftrs, web_ftr, axis=0)
                web_bin_bads = np.append(web_bin_bads, web_bin_bad)
                web_bin_goods = np.append(web_bin_goods, web_bin_good)
    np.save('web_ftrs_wht_xi.npy', web_ftrs)
    np.save('web_bin_bad_wht_xi.npy', web_bin_bads)
    np.save('web_bin_good_wht_xi.npy', web_bin_goods)
    first_loop = True
    web_ftrs = None
    web_bin_bads = None
    web_bin_goods = None
    for page_web in my_pages_all:
        boxes = DetectedBox.filter(parent_page=page_web)
        if len(boxes) > 0:
            web_ftr, web_bin_bad, web_bin_good = build_np(boxes)
            if first_loop:
                web_ftrs = web_ftr
                web_bin_bads = web_bin_bad
                web_bin_goods = web_bin_good
                first_loop = False
            else:
                web_ftrs = np.append(web_ftrs, web_ftr, axis=0)
                web_bin_bads = np.append(web_bin_bads, web_bin_bad)
                web_bin_goods = np.append(web_bin_goods, web_bin_good)
    np.save('web_ftrs_xi.npy', web_ftrs)
    np.save('web_bin_bad_xi.npy', web_bin_bads)
    np.save('web_bin_good_xi.npy', web_bin_goods)


class Migration(migrations.Migration):

    dependencies = [
        ('calligraphy', '0231_auto_20171012_1448'),
    ]

    operations = [ migrations.RunPython(do_stuff)
    ]
