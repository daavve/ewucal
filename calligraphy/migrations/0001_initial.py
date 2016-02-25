# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-25 21:28
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion
import os
import socket
import json

HOSTNAME = socket.gethostname()
if HOSTNAME == 'bigArch':
    IMAGE_DIR = "/home/dave/workspace/pycharm/fetch/grabbedBooks/"
else:
    IMAGE_DIR = "/media/pages/"


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
                ('char_image', models.ImageField(blank=True, storage=django.core.files.storage.FileSystemStorage(), upload_to='')),
                ('parent_author', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='calligraphy.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_image', models.ImageField(blank=True, storage=django.core.files.storage.FileSystemStorage(), upload_to='')),
                ('page_transcript', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('work_id', models.IntegerField(primary_key=True, serialize=False)),
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
        migrations.AddField(
            model_name='character',
            name='parent_work',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='calligraphy.Work'),
        ),
        migrations.RunPython(import_data)
    ]
