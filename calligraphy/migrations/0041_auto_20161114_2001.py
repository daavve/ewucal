# -*- coding: utf-8 -*-
#
# Goes through and creates new thumbnails 200px high instead of 100px
#
##########################################################
from __future__ import unicode_literals

from django.db import migrations, models
from PIL import Image
from pathlib import Path

def make_thumbnails(apps) -> None:
    Character = apps.get_model('calligraphy', 'Character')
    chars = Character.objects.all()
    for char in chars:
        fileptr = char.image_high_rez
        if not bool(fileptr):
            raise Exception('cannot crop an iamge that does not exist')
        fileptr.close()
        im = Image.open(str(char.image_high_rez))
        width = int(float(char.x2 - char.x1) / float(char.y2 - char.y1) * 200)
        img_thumb = im.resize((width, 200), Image.BOX)
        img_thumb_name = str(char.image).strip('jpgpntif') + 'thumb.png'
        img_thumb.save(img_thumb_name, 'PNG')
        img_thumb.close()
        char.image_thumb = img_thumb_name
        char.image_thumb_y = 200
        char.image_thumb_x = width
        char.save()

def do_stuff(apps, schemd_editor) -> None:
    make_thumbnails(apps)


class Migration(migrations.Migration):

    dependencies = [
        ('calligraphy', '0040_page_i_transform_validated'),
    ]

    operations = [ migrations.RunPython(do_stuff)
    ]
