from django.db import models


class Book(models.Model):
    book_id = models.IntegerField(primary_key=True)
    book_title = models.CharField(max_length=16)
    book_author = models.CharField(max_length=16)
    book_transcriber = models.CharField(max_length=16,blank=True)
    book_notes = models.TextField(blank=True)


class Page(models.Model):
    page_number = models.IntegerField()
    book_parent = models.ForeignKey(Book, on_delete=models.CASCADE)
    book_notes = models.TextField(blank=True)


class Character(models.Model):
    page_parent = models.ForeignKey(Page, on_delete=models.CASCADE)
    char_mark = models.CharField(max_length=4, blank=True)
    x1 = models.IntegerField()
    y1 = models.IntegerField()
    x2 = models.IntegerField()
    y2 = models.IntegerField()
    char_notes = models.TextField(blank=True)



