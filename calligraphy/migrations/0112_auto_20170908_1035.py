# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-08 10:35
from __future__ import unicode_literals

from skimage import color, io, filters, measure
from scipy import ndimage
import numpy as np

from django.db import migrations

def do_stuff(apps, schemd_editor) -> None:
    Pages = apps.get_model('calligraphy', 'Page').objects
    HaveChars = apps.get_model('calligraphy', 'PagesHaveChars').objects
    Characters = apps.get_model('calligraphy', 'Character').objects
    DetectedBox = apps.get_model('calligraphy', 'DetectedBox')
    for thisPage in HaveChars.all():
        curPage = Pages.get(id=thisPage.haveChars.id)
        chars = Characters.filter(parent_page=curPage)
        x_1 = 9999999999
        x_2 = 0
        y_1 = 9999999999
        y_2 = 0
        for char in chars:
            if x_1 > char.x1:
                x_1 = char.x1
            if y_1 > char.y1:
                y_1 = char.y1
            if x_2 < char.x2:
                x_2 = char.x2
            if y_2 < char.y2:
                y_2 = char.y2
        if curPage.image_works:
            img_str = str(curPage.image)
            orimg = color.rgb2grey(io.imread(img_str))
            timg = orimg[y_1:y_2, x_1:x_2]
            print(img_str + " " + str(timg.shape))
            if timg.size < 100:
                timg = orimg
            BIGGEST_ALLOWABLE_CHAR = 1000000
            img = ndimage.gaussian_filter(timg, 1) # gets rid of the worst noise
            SEGMENTS = 5 #eg: 5^2=25
            SUBSEGMENTS = 5
            WEIGHT_TOP = 3 # Final picture calculated (TOP * val_top + MID * val_mid + BOT * val_bot) / (TOP + MID + BOT)
            WEIGHT_MIDDLE = 2
            WEIGHT_BOTTOM = 1
            img_threshold = np.zeros_like(img)
            IMG_LEN = img.shape[0]
            IMG_WID = img.shape[1]
            I_STRIDE= int(IMG_LEN / SEGMENTS)
            I_STRIDE_M = int(I_STRIDE / SUBSEGMENTS)
            J_STRIDE = int(IMG_WID / SEGMENTS)
            J_STRIDE_M = int(J_STRIDE / SUBSEGMENTS)
            threshold_top = filters.threshold_li(img)
            threshold_top_weighted = threshold_top * WEIGHT_TOP
            for i in range(0, IMG_LEN, I_STRIDE):
                i_box = min(IMG_LEN, i + I_STRIDE)
                for j in range(0, IMG_WID, J_STRIDE):
                    j_box = min(IMG_WID, j + J_STRIDE)
                    subimage = img[i:i_box, j:j_box]
                    if subimage.min() == subimage.max():
                        img_threshold[i:i_box, j:j_box].fill(threshold_top)
                    else:
                        threshold_middle_weighted = filters.threshold_li(subimage) * WEIGHT_MIDDLE + threshold_top_weighted
                        for i_sub in range(i, i_box, I_STRIDE_M):
                            i_box_m = min(i_box, i_sub + I_STRIDE_M)
                            for j_sub in range(j, j_box, J_STRIDE_M):
                                j_box_m = min(j_box, j_sub + J_STRIDE_M)
                                subsubimage = img[i_sub:i_box_m, j_sub:j_box_m]
                                if subsubimage.min() == subsubimage.max():
                                    this_threshold = int(threshold_middle_weighted / (WEIGHT_TOP + WEIGHT_MIDDLE))
                                else:
                                    this_threshold = int((threshold_middle_weighted + filters.threshold_li(subsubimage) * WEIGHT_BOTTOM) / (WEIGHT_TOP + WEIGHT_MIDDLE + WEIGHT_BOTTOM))
                                img_threshold[i_sub:i_box_m, j_sub:j_box_m].fill(this_threshold)
            bw = img > img_threshold
            bw_i = img < img_threshold
            labels = measure.label(bw, connectivity=2)
            labels_i = measure.label(bw_i, connectivity=2)
            lbl_props = measure.regionprops(labels)
            lbl_props_i = measure.regionprops(labels_i)
            for lbl_prop in lbl_props:
                bbox = lbl_prop.bbox
                area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
                if area < BIGGEST_ALLOWABLE_CHAR:
                    print(bbox)
                    y1 = bbox[0] + y_1
                    y2 = bbox[2]
                    x1 = bbox[1] + x_1
                    x2 = bbox[3]
                    centroid = lbl_prop.local_centroid
                    DetectedBox(parent_page = curPage,
                                black_chars = False,
                                area = lbl_prop.area,
                                convex_area = lbl_prop.convex_area,
                                eccentricity = lbl_prop.eccentricity,
                                extant = lbl_prop.extent,
                                x1 = x1,
                                x2 = x2,
                                y1 = y1,
                                y2 = y2,
                                major_axis_length = lbl_prop.major_axis_length,
                                minor_axis_length = lbl_prop.minor_axis_length,
                                orientation = lbl_prop.orientation,
                                solidity = lbl_prop.solidity,
                                local_centroid_x = centroid[1],
                                local_centroid_y = centroid[0]).save()
            for lbl_prop in lbl_props_i:
                bbox = lbl_prop.bbox
                area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
                if area < BIGGEST_ALLOWABLE_CHAR:
                    print(bbox)
                    y1 = bbox[0] + y_1
                    y2 = bbox[2]
                    x1 = bbox[1] + x_1
                    x2 = bbox[3]
                    centroid = lbl_prop.local_centroid
                    DetectedBox(parent_page = curPage,
                                black_chars = True,
                                area = lbl_prop.area,
                                convex_area = lbl_prop.convex_area,
                                eccentricity = lbl_prop.eccentricity,
                                extant = lbl_prop.extent,
                                x1 = x1,
                                x2 = x2,
                                y1 = y1,
                                y2 = y2,
                                major_axis_length = lbl_prop.major_axis_length,
                                minor_axis_length = lbl_prop.minor_axis_length,
                                orientation = lbl_prop.orientation,
                                solidity = lbl_prop.solidity,
                                local_centroid_x = centroid[1],
                                local_centroid_y = centroid[0]).save()

class Migration(migrations.Migration):

    dependencies = [
        ('calligraphy', '0111_auto_20170908_1032'),
    ]

    operations = [ migrations.RunPython(do_stuff)
    ]
