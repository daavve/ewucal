# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-28 23:27
#
#
# Goes through an builds pairs of features and whether they are part of the same char
#
###########################################################
from __future__ import unicode_literals

from django.db import migrations
import numpy as np
 
class Box(object):
    def __init__(self, parent):
        self.parent = parent
        self.nearby_boxes = []
        self.y_range = set()
        for i in range(parent.y1, parent.y2):
            self.y_range.add(i)
 
class BoxIndex(object):
    def __init__(self):
        self.boxes_id = set()

def build_np(boxes, nearby, same_char):
    features = np.zeros((len(boxes), 22), dtype=np.int32)
    same_char = np.zeros(len(boxes), dtype=np.bool)
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
        features[i][10] = int((boxes[i].y1 - nearby.parent.y1) * 2147483647 /  curPage.image_length)
        features[i][11] = int((boxes[i].x1 - nearby.parent.x1) * 2147483647 /  curPage.image_width)
        features[i][12] = nearby.parent.area_norm
        features[i][13] = nearby.parent.eccentricity_norm
        features[i][14] = nearby.parent.solidity_norm
        features[i][15] = nearby.parent.orientation_norm
        features[i][16] = nearby.parent.li_threshold_bottom_norm
        features[i][17] = nearby.parent.li_threshold_top_norm
        features[i][18] = nearby.parent.local_centroid_x_norm
        features[i][19] = nearby.parent.local_centroid_y_norm
        features[i][20] = nearby.parent.major_axis_length_norm
        features[i][21] = nearby.parent.minor_axis_length_norm

def compare_boxes(box, boxcomp):
    same_char = False
    if box.parent_char:
        if boxcomp.parent_char:
            if box.parent_char.id == boxcomp.parent_char.id:
                same_char = True
    

NUM_NEARBY_GLYPHS = 1

def do_stuff(apps, schemd_editor):
    Pages = apps.get_model('calligraphy', 'Page').objects
    DetectedBox = apps.get_model('calligraphy', 'DetectedBox').objects
    PagesHaveChars = apps.get_model('calligraphy', 'PagesHaveChars').objects
    page_count = len(PagesHaveChars.all())
    count = 0
    for thisPage in PagesHaveChars.all():
        count += 1
        print(str(count) + " / " + str(page_count))
        cur_page = Pages.get(id=thisPage.haveChars.id)
        boxes  = DetectedBox.filter(parent_page=cur_page)
        x_index = dict()
        box_by_id = dict()
        box_list = []
        my_x_boxes = set()
        for i in range(cur_page.image_length):
            x_index[i] = BoxIndex()
        for box in boxes:
            mybox = Box(box)
            box_list.append(mybox)
            box_by_id[box.id] = mybox
            for i in range(box.x1, box.x2):
                x_index[i].boxes_id.add(box.id)
        for box in box_list:
            cur_x = box.parent.x2
            cur_y = box.parent.y2
            edge_right = False
            edge_bottom = False
            chars_x = set()
            chars_x_ys = set()
            chars_confirmed = set()
            y_range = set()
            while len(chars_confirmed) < NUM_NEARBY_GLYPHS and not (edge_right and edge_bottom):
                if not edge_right:
                    cur_x += 1
                    if cur_x > cur_page.image_width:
                        edge_right = True
                    else:
                        if len(x_index[cur_x].boxes_id):
                            diff = x_index[cur_x].boxes_id.difference(chars_x)
                            if diff:
                                chars_x.update(diff)
                                for dif in diff:
                                    chars_x_ys.update(box_by_id[dif].y_range)
                if not edge_bottom:
                    cur_y += 1
                    if cur_y > cur_page.image_length:
                        edge_bottom = True
                    else:
                        y_range.add(cur_y)
                if chars_x_ys.intersection(y_range):
                    for char_cur in chars_x:
                        if box_by_id[char_cur].y_range.intersection(y_range):
                            chars_confirmed.add(char_cur)
            for boxcomp in chars_confirmed:
                compare_boxes(box.parent, box_by_id[boxcomp].parent)
    raise Exception("stop here")


class Migration(migrations.Migration):

    dependencies = [
        ('calligraphy', '0236_auto_20171027_0008'),
    ]

    operations = [ migrations.RunPython(do_stuff)
    ]
