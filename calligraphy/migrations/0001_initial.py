# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-23 01:19
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion
import json, socket, os
from django.core import files

from django.core.files.storage import FileSystemStorage



HOSTNAME = socket.gethostname()
if HOSTNAME == 'ewucal_server' or HOSTNAME == 'calligraphy.ewuthesis.com':
    IMAGE_DIR = "/home/django/CADAL-scripts/fetchimages/workslist/grabbedBooks/"
else:
    IMAGE_DIR = "/home/dave/workspace/pycharm/fetch/grabbedBooks/"


def read_cworks(apps) -> None:
    jsonfile = open("c-works.json", mode="r", encoding='utf-8')
    readfile = json.load(jsonfile)
    jsonfile.close()
    Author = apps.get_model("calligraphy", "Author")
    Work = apps.get_model("calligraphy", "Work")
    Page = apps.get_model("calligraphy", "Page")
    for r in readfile:
        name = r['name']
        dynesty = r['dynesty']
        if dynesty == '':
            d_author = Author(author_name=name)
        else:
            d_author = Author(author_name=name, author_dynesty=dynesty)
        d_author.save()
        for w in r['works']:
            text_block = w['text_block'].strip('\n')
            if text_block == '':
                d_work = Work(work_author=d_author)
            else:
                d_work = Work(work_author=d_author, work_transcript=text_block)
            d_work.save()
            imgprefix = str(w['pages']['book_id'])
            for p in w['pages']['pages_id']:
                fileimg = IMAGE_DIR + imgprefix + "-" + str(p)
                if not os.path.isfile(fileimg):
                    fileimg = fileimg.split('.')[0] + ".tif"
                    if not os.path.isfile(fileimg):
                        fileimg = fileimg.split('.')[0] + ".png"
                        if not os.path.isfile(fileimg):
                            raise Exception('Cannot find required image file', fileimg.split('.')[0])
                d_page = Page(parent_work=d_work, page_image=fileimg)
                d_page.save
#                os.remove(fileimg)
#  We might run out of room here, but I think its ok

def import_data(apps, schemd_editor):
    read_cworks(apps)



class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(max_length=64)),
                ('author_dynesty', models.CharField(blank=True, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('char_mark', models.CharField(blank=True, max_length=64)),
                ('x1', models.IntegerField(blank=True)),
                ('y1', models.IntegerField(blank=True)),
                ('x2', models.IntegerField(blank=True)),
                ('y2', models.IntegerField(blank=True)),
                ('char_image', models.ImageField(blank=True, storage=FileSystemStorage())),
                ('parent_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calligraphy.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_image', models.ImageField(blank=True, storage=FileSystemStorage())),
            ],
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_transcript', models.TextField(blank=True)),
                ('work_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calligraphy.Author')),
            ],
        ),
        migrations.AddField(
            model_name='page',
            name='parent_work',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='calligraphy.Work'),
        ),
        migrations.AddField(
            model_name='character',
            name='parent_page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calligraphy.Page'),
        ),
        migrations.RunPython(import_data)
    ]
