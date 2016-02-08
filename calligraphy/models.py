from django.db import models


class Collection(models.Model):
    collection_name = models.CharField(max_length=16)


class Book(models.Model):
    parent_collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    book_title = models.CharField(max_length=16,blank=True)
    book_author = models.CharField(max_length=16,blank=True)
    book_transcriber = models.CharField(max_length=16,blank=True)
    book_notes = models.TextField(blank=True)


class Page(models.Model):
    page_number = models.IntegerField()
    parent_book = models.ForeignKey(Book, on_delete=models.CASCADE)
    page_notes = models.TextField(blank=True)
    page_image = models.ImageField(blank=True, upload_to='images/pages/')


class Character(models.Model):
    parent_page = models.ForeignKey(Page, on_delete=models.CASCADE)
    char_mark = models.CharField(max_length=4, blank=True)
    x1 = models.IntegerField(blank=True)
    y1 = models.IntegerField(blank=True)
    x2 = models.IntegerField(blank=True)
    y2 = models.IntegerField(blank=True)
    char_notes = models.TextField(blank=True)
    char_image = models.ImageField(blank=True, upload_to='images/characters/')



