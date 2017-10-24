# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-19 00:08
#
# writes groups of features in a neighborhood to disk,
# It takes too long to write all white chars to disk so we just do the wang-xi and scanned sets 
# Also the resulting classifier is no better than random
#
#######################################################################

from __future__ import unicode_literals

from django.db import migrations
import numpy as np

class Box(object):
    def __init__(self, parent):
        self.parent = parent
        self.area   = (parent.x2 - parent.x1) * (parent.y2 - parent.y1)
        self.mid_x = int((parent.x2 - parent.x1) / 2) + parent.x1
        self.mid_y = int((parent.y2 - parent.y1) / 2) + parent.y1
        self.nearby_boxes = []
        self.x_range = set()
        self.y_range = set()
        for i in range(parent.y1, parent.y2):
            self.y_range.add(i)

class BoxIndex(object):
    def __init__(self):
        self.boxes_id = set()


def build_np(boxes, nearbys, curPage, k_num):
    FEATURE_SIZE = 10 + ( 2 + 10 ) * k_num
    features = np.zeros((len(boxes), FEATURE_SIZE), dtype=np.int32)
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
        ctr = 10
        for nearby in nearbys[i]:
            features[i][ctr + 0] = int((boxes[i].y1 - nearby.parent.y1) * 2147483647 /  curPage.image_length)
            features[i][ctr + 1] = int((boxes[i].x1 - nearby.parent.x1) * 2147483647 /  curPage.image_width)
            features[i][ctr + 2] = nearby.parent.area_norm
            features[i][ctr + 3] = nearby.parent.eccentricity_norm
            features[i][ctr + 4] = nearby.parent.solidity_norm
            features[i][ctr + 5] = nearby.parent.orientation_norm
            features[i][ctr + 6] = nearby.parent.li_threshold_bottom_norm
            features[i][ctr + 7] = nearby.parent.li_threshold_top_norm
            features[i][ctr + 8] = nearby.parent.local_centroid_x_norm
            features[i][ctr + 9] = nearby.parent.local_centroid_y_norm
            features[i][ctr + 10] = nearby.parent.major_axis_length_norm
            features[i][ctr + 11] = nearby.parent.minor_axis_length_norm
            ctr += 12
    return features, bin_bad, bin_good


# Find nearby boxes
def find_nearby_boxes(boxes, cur_page):
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
        MID_X = box.mid_x
        MID_Y = box.mid_y
        edge_right = False
        edge_left = False
        edge_top = False
        edge_bottom = False
        offset = 1
        chars_x = set()
        chars_confirmed = set()
        y_range = set()
        y_range.add(MID_Y)
        while len(char_set) < 5:
            if not edge_right:
                new_x1 = MID_X - offset
                if new_x1 < 0 :
                    edge_right = True
                else:
                    chars_x.update(x_index[new_x1].boxes_id)
            if not edge_left:
                new_x2 = MID_X + offset
                if new_x2 > cur_page.image_width:
                    edge_left = True
            if not edge_top:
                new_y1 = MID_Y - offset
                if new_y1 < 0:
                    edge_top = True
                else:
                    y_range.add(new_y1)
            if not edge_bottom:
                new_y2 = MID_Y + offset
                if new_y2 > cur_page.image_length:
                    edge_bottom = True:
                else:
                    y_range.add(new_y2)
            offset += 1
            

        
    #return build_np(boxes, nearbys, curPage, k_num)


        

def do_stuff(apps, schemd_editor):
    DetectedBox = apps.get_model('calligraphy', 'DetectedBox').objects
    my_author = apps.get_model('calligraphy', 'Author').objects.get(id=15) # 王羲之
    my_works = apps.get_model('calligraphy', 'Work').objects.filter(author=my_author)
    my_pages_xi = apps.get_model('calligraphy', 'Page').objects.filter(has_copyright_restrictions=False, black_chars=False, parent_author=my_author)
    my_pages_wht = apps.get_model('calligraphy', 'Page').objects.filter(has_copyright_restrictions=False, black_chars=False)
    my_pages_scn = apps.get_model('calligraphy', 'Page').objects.filter(has_copyright_restrictions=True)
    web_ftrs = None
    web_bin_bads = None
    web_bin_goods = None
    for k_num in range(10):
        first_loop = True
        for page_web in my_pages_xi:
            boxes = DetectedBox.filter(parent_page=page_web)
            if len(boxes) > 0:
                find_nearby_boxes(boxes, page_web)
    #            web_ftr, web_bin_bad, web_bin_good = find_nearby_boxes(boxes, page_web, k_num)
    #            if first_loop:
    #                 web_ftrs = web_ftr
    #                web_bin_bads = web_bin_bad
    #                web_bin_goods = web_bin_good
    #                first_loop = False
    #            else:
    #                web_ftrs = np.append(web_ftrs, web_ftr, axis=0)
    #                web_bin_bads = np.append(web_bin_bads, web_bin_bad)
    #                web_bin_goods = np.append(web_bin_goods, web_bin_good)
    #    saveName = "xi-" + str(k_num) + "-my_pages.npy"
    #    np.save(saveName, web_ftrs)
    #np.save("xi-bin-good_my_pages.npy", web_bin_goods)
    #np.save("xi-bin-bad_my_pages.npy", web_bin_bads)
    #for k_num in range(10):
    #    first_loop = True
    #    for page_web in my_pages_wht:
    #        boxes = DetectedBox.filter(parent_page=page_web)
    #        if len(boxes) > 0:
    #            web_ftr, web_bin_bad, web_bin_good = find_nearby_boxes(boxes, page_web, k_num)
    #            if first_loop:
    #                web_ftrs = web_ftr
    #                web_bin_bads = web_bin_bad
    #                web_bin_goods = web_bin_good
    #                first_loop = False
    #            else:
    #                web_ftrs = np.append(web_ftrs, web_ftr, axis=0)
    #                web_bin_bads = np.append(web_bin_bads, web_bin_bad)
    #                web_bin_goods = np.append(web_bin_goods, web_bin_good)
    #    saveName = "wht-" + str(k_num) + "-my_pages.npy"
    #    np.save(saveName, web_ftrs)
    #np.save("wht-bin-good_my_pages.npy", web_bin_goods)
    #np.save("wht-bin-bad_my_pages.npy", web_bin_bads)
    #for k_num in range(10):
    #    first_loop = True
    #    for page_web in my_pages_scn:
    #        boxes = DetectedBox.filter(parent_page=page_web)
    #        if len(boxes) > 0:
    #            web_ftr, web_bin_bad, web_bin_good = find_nearby_boxes(boxes, page_web, k_num)
    #            if first_loop:
    #                web_ftrs = web_ftr
    #                web_bin_bads = web_bin_bad
    #                web_bin_goods = web_bin_good
    #                first_loop = False
    #            else:
    #                web_ftrs = np.append(web_ftrs, web_ftr, axis=0)
    #                web_bin_bads = np.append(web_bin_bads, web_bin_bad)
    #                web_bin_goods = np.append(web_bin_goods, web_bin_good)
    #    saveName = "scn-" + str(k_num) + "-my_pages.npy"
    #    np.save(saveName, web_ftrs)
    #    np.save("scn-bin-good_my_pages.npy", web_bin_goods)
    #    np.save("scn-bin-bad_my_pages.npy", web_bin_bads)
    raise Exception("STOP HERE")






class Migration(migrations.Migration):

    dependencies = [
        ('calligraphy', '0232_auto_20171012_1459'),
    ]

    operations = [ migrations.RunPython(do_stuff)
    ]
