# -*- coding: utf-8 -*-
#
# This one connects all charsets to archive characters so we don't loose information
#
########################################################################################
from __future__ import unicode_literals

from django.db import migrations

def change_ref(apps) -> None:
    Chars_back = apps.get_model('calligraphy', 'Character_orig')
    Chars =      apps.get_model('calligraphy', 'Character')
    CharSet =    apps.get_model('calligraphy', 'CharSet')
    
    for charset in CharSet.objects.all():
        replacement_chars = []
        for char in charset.set_chars.all():
            replacement_chars.append(Chars_back.objects.get(id=char.id))
        charset.set_chars_orig.set(replacement_chars)

def do_stuff(apps, schemd_editor) -> None:
    change_ref(apps)


class Migration(migrations.Migration):

    dependencies = [
        ('calligraphy', '0089_charset_set_chars_orig'),
    ]

    operations = [ migrations.RunPython(do_stuff)
    ]
