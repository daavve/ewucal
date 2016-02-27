from django.db import models
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage()


class Author(models.Model):
    author_name = models.CharField(max_length=64)
    author_dynesty = models.CharField(max_length=64, blank=True)


class Work(models.Model):
    work_id = models.IntegerField(primary_key=True)
    work_title = models.CharField(max_length=64, blank=True)
    work_author = models.ForeignKey(Author)
    work_transcript = models.TextField(blank=True)


class Page(models.Model):
    page_bookid = models.IntegerField(null=True)
    page_pageid = models.IntegerField(null=True)
    page_image = models.ImageField(blank=True, storage=fs)
    parent_work = models.ForeignKey(Work, null=True)
    page_transcript = models.TextField(blank=True)


class Character(models.Model):
    parent_page = models.ForeignKey(Page)
    x1 = models.IntegerField(blank=True)
    y1 = models.IntegerField(blank=True)
    x2 = models.IntegerField(blank=True)
    y2 = models.IntegerField(blank=True)
    char_image = models.ImageField(blank=True, storage=fs)
