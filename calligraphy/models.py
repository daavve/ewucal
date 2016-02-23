from django.db import models
from django.core.files.storage import FileSystemStorage
from socket import gethostname

# filestorage needs to be outside project path, or pycharm will index the pictures.  This is slow.
HOSTNAME = gethostname()
if HOSTNAME == 'ewucal_server' or HOSTNAME == 'calligraphy.ewuthesis.com':
    fs = FileSystemStorage(location='images')
else:
    fs = FileSystemStorage(location='~/workspace/pycharm/ewucal_images/')


class Author(models.Model):
    author_name = models.CharField(max_length=16)
    author_dynesty = models.CharField(max_length=16, blank=True)


class Work(models.Model):
    work_author = models.ForeignKey(Author)
    work_transcript = models.TextField(blank=True)


class Page(models.Model):
    page_image = models.ImageField(blank=True, storage=fs)
    parent_work = models.ForeignKey(Work, blank=True)


class Character(models.Model):
    parent_page = models.ForeignKey(Page)
    parent_author = models.ForeignKey(Author)
    char_mark = models.CharField(max_length=4, blank=True)
    x1 = models.IntegerField(blank=True)
    y1 = models.IntegerField(blank=True)
    x2 = models.IntegerField(blank=True)
    y2 = models.IntegerField(blank=True)
    char_image = models.ImageField(blank=True, storage=fs)
