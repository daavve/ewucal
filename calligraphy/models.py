from django.db import models
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage()


class Author(models.Model):
    author_name = models.CharField(max_length=64)
    author_dynesty = models.CharField(max_length=64, blank=True)


class Work(models.Model):
    work_author = models.ForeignKey(Author)
    work_transcript = models.TextField(blank=True)


class Page(models.Model):
    page_image = models.ImageField(blank=True, storage=fs)
    parent_work = models.ForeignKey(Work, blank=True)
    page_transcript = models.TextField(blank=True)


class Character(models.Model):
    parent_page = models.ForeignKey(Page)
    parent_author = models.ForeignKey(Author, blank=True)
    parent_work = models.ForeignKey(Work, blank=True)
    char_mark = models.CharField(max_length=64, blank=True)
    x1 = models.IntegerField(blank=True)
    y1 = models.IntegerField(blank=True)
    x2 = models.IntegerField(blank=True)
    y2 = models.IntegerField(blank=True)
    char_image = models.ImageField(blank=True, storage=fs)
