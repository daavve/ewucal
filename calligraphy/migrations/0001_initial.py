# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-09 19:54
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


from django.db import migrations, models
import django.db.models.deletion

from django.core.files import File


import json, os, stat
from builtins import bool


class Charjson(object):
    def __init__(self, mark: str, author: str, work: str, work_id: str, page_id: str, coordinates: [str]):
        self.chi_mark = mark
        self.chi_author = author
        self.chi_work = work
        self.work_id = work_id
        self.page_id = page_id
        self.xy_coordinates = coordinates


class Library(object):
    def __init__(self, title: str):
        self.title = title
        self.collections = []


class Collection(object):
    def __init__(self, title: str):
        self.title = title
        self.books = []

    def addnewbook(self, newchar: Charjson) -> None:
        newbook = Book(int(newchar.work_id), newchar.chi_work, newchar.chi_author, self.title)
        newbook.addchar(newchar)
        self.books.append(newbook)

    def addchar(self, newchar: Charjson, have_page_image: bool) -> None:
        if len(self.books) >= 1:
            foundbook = False
            for book in self.books:
                if book.bid == int(newchar.work_id):
                    book.addchar(newchar)
                    foundbook = True
                    break
            if not foundbook:
                self.addnewbook(newchar)
        else:
            self.addnewbook(newchar)

    def addpagetobook(self, newpage: Charjson) -> None:
        newbook = Book(int(newpage.work_id), newpage.chi_work, newpage.chi_author, self.title)
        newbook.addpage(newpage)
        self.books.append(newbook)

    def addpage(self, newpage: Charjson) -> None:
        if len(self.books) >= 1:
            foundbook = False
            for book in self.books:
                if book.bid == int(newpage.work_id):
                    book.addpage(newpage)
                    foundbook = True
                    break
            if not foundbook:
                self.addpagetobook(newpage)
        else:
            self.addpagetobook(newpage)


class Book(object):
    def __init__(self, bid: int, title: str, author: str, collection: str) -> None:
        self.bid = bid
        self.title = title
        self.author = author
        self.pages = []
        self.collection = collection

    def addnewpage(self, newchar: Charjson, have_page_image: bool) -> None:
        newpage = Page(int(newchar.page_id), self.bid, self.collection, have_page_image)
        newpage.addchar(newchar)
        self.pages.append(newpage)

    def addchar(self, newchar: Charjson, have_page_image: bool) -> None:
        if len(self.pages) >= 1:
            foundpage = False
            for page in self.pages:
                if page.number == int(newchar.page_id):
                    foundpage = True
                    page.addchar(newchar)
                    break
            if not foundpage:
                self.addnewpage(newchar, have_page_image)
        else:
            self.addnewpage(newchar, have_page_image)

    def addpage(self, newpage: Charjson) -> None:
        if len(self.pages) >= 1:
            foundpage = False
            for page in self.pages:
                if page.number == int(newpage.page_id):
                    foundpage = True
                    break
            if not foundpage:
                self.pages.append(Page(int(newpage.page_id), self.bid, self.collection))
        else:
            self.pages.append(Page(int(newpage.page_id), self.bid, self.collection))


class Page(object):
    def __init__(self, number: int, bid: int, collection: str, have_page_image: bool):
        self.number = number
        self.bid = bid
        self.collection = collection
        self.characters = []
        self.have_page_image = have_page_image

    def getfilepath(self) -> str:
        if self.collection == 'cadal':
            bookpath = '{:08d}'.format(self.bid) + '/'
            pagepath = '{:08d}'.format(self.number) + '.jpg'
            return "fetch/" + self.collection + '/books/' + bookpath + pagepath
        else:
            return "fetch/" + self.collection + '/' + str(self.bid) + '/' + str(self.number) + 'i.png'

    def addnewchar(self, newchar: Charjson) -> None:
        if newchar.xy_coordinates[0] == '?':
            self.characters.append(Character(newchar.chi_mark, 0, 0, 0, 0, self.bid, self.number, self.collection))
        else:
            self.characters.append(Character(newchar.chi_mark, int(newchar.xy_coordinates[0]),
                                                               int(newchar.xy_coordinates[1]),
                                                               int(newchar.xy_coordinates[2]),
                                                               int(newchar.xy_coordinates[3]),
                                                                   self.bid,
                                                                   self.number,
                                                                   self.collection))

    def addchar(self, newchar: Charjson) -> None:
        if len(self.characters) >= 1:
            foundchar = False
            if newchar.xy_coordinates[0] == '?':
                self.addnewchar(newchar)
            else:
                for chara in self.characters:
                    if int(newchar.xy_coordinates[0]) == chara.x1 and int(newchar.xy_coordinates[1]) == chara.y1 and int(newchar.xy_coordinates[2]) == chara.x2 and int(newchar.xy_coordinates[3]) == chara.y2:
                        foundchar = True
                        break
                if not foundchar:
                    self.addnewchar(newchar)
        else:
            self.addnewchar(newchar)


class Character(object):
    def __init__(self, mark: str, x1: int, y1: int, x2: int, y2: int, bookid: int, pageid: int, collection: str):
        self.mark = mark
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.pageid = pageid
        self.bookid = bookid
        self.collection = collection

    def getfilepath(self) -> str:
        bookpath = '{:08d}'.format(self.bookid) + '/'
        charfront = '{:08d}'.format(self.pageid) + '('
        charrear = str(self.x1) + ',' + str(self.y1) + ',' + str(self.x2) + ',' + str(self.y2) + ').jpg'
        return "fetch/" + self.collection + '/characterimage/' + bookpath + charfront + charrear


def readjson(filename: str) -> [Charjson]:  # Not too bad, less than 70M
    jsonfile = open(filename, "r")
    readfile = json.load(jsonfile)
    jsonfile.close()
    characters = []
    for r in readfile:
        characters.append(
            Charjson(r['chi_mark'], r['chi_author'], r['chi_work'], r['work_id'], r['page_id'], r['xy_coordinates']))
    return characters

ROOTDIR = "fetch/"
HTMDIR = "charDataHTML/"
BOOKSDIR = "cadal/books/"
CHARDIR = "cadal/characterimage/"


def getcharsbyfilename() -> [Charjson]:
    charfiles = []
    for f in os.listdir(ROOTDIR + CHARDIR):
        pathname = os.path.join(ROOTDIR + CHARDIR, f)
        booknum = str(pathname).split('/')[3]
        if stat.S_ISDIR(os.stat(pathname).st_mode):
            for img in os.listdir(pathname):
                if img.endswith('.jpg'):
                    imgs = img.split('(')
                    pagenum = imgs[0]
                    coords = imgs[1].strip(').jpg').split(',')
                    charfiles.append(Charjson("?", "?", "?", booknum, pagenum, coords))
    return charfiles


def getpages() -> [Charjson]:  # I know cut / paste coding is bad, but i'm in a hurry
    imgfiles = []
    for f in os.listdir(ROOTDIR + BOOKSDIR):
        pathname = os.path.join(ROOTDIR + BOOKSDIR, f)
        booknum = str(pathname).split('/')[3]
        if stat.S_ISDIR(os.stat(pathname).st_mode):
            for img in os.listdir(pathname):
                if img.endswith('.jpg'):
                    imgname = img.strip('.jpg')
                    imgfiles.append(Charjson("?", "?", "?", booknum, imgname, ['?']))
    return imgfiles

KOSUKEDIR = "scanned/1"


def getpagesfromkosukebook() -> [Charjson]:  # I know cut / paste coding is bad, but i'm in a hurry
    imgfiles = []
    pathname = os.path.join(ROOTDIR + KOSUKEDIR)
    booknum = str(pathname).split('/')[2]
    for img in os.listdir(pathname):
        if img.endswith('i.png'):
            imgname = img.strip('i.png')
            imgfiles.append(Charjson("?", "王羲之", "集字聖教序 東普", booknum, imgname, ['?']))
    return imgfiles

CHARTXTFILE = "fetch/scanned/1/tesseract_convert.txt"
NOTCHARS = "﹒。o‵‧ ˙\n"


def txt2char() -> [Charjson]:
    charsinpage = []
    f = open(CHARTXTFILE, encoding="utf-8")
    filebuff = f.read()
    f.close()
    filebuff = filebuff.split('##########################################')[1]
    filebuff = filebuff.split('STOP!')[0]
    filebuff = filebuff.split('-----------------------')
    for scannedpage in filebuff:
        pagesplit = scannedpage.split('t.png')
        pagenum = pagesplit[0].strip('\n')
        pagechars = pagesplit[1]
        for char in pagechars:
            if NOTCHARS.count(char) == 0:
                charsinpage.append(Charjson(char, "王羲之", "集字聖教序", 1, pagenum, ['?']))
    return charsinpage


def import_data(apps, schema_editor):
    Coldb = apps.get_model("calligraphy", "Collection")
    Bookdb = apps.get_model("calligraphy", "Book")
    Pagedb = apps.get_model("calligraphy", "Page")
    Chardb = apps.get_model("calligraphy", "Character")
    library = Library("Calligraphy")
    library.collections.append(Collection("cadal"))
    library.collections.append(Collection("scanned"))
    chars = readjson('dump.json')
    for char in chars:
        library.collections[0].addchar(char, True)
    filechars = getcharsbyfilename()
    for char in filechars:
        library.collections[0].addchar(char, False)
    pageonly = getpages()
    for page in pageonly:
        library.collections[0].addpage(page)
    kosukepage = getpagesfromkosukebook()
    for page in kosukepage:
        library.collections[1].addpage(page)
    txtchar = txt2char()
    for char in txtchar:
        library.collections[1].addchar(char, True)

    for collection in library.collections:
        curcollect = Coldb(collection_name=collection.title)
        curcollect.save()
        for book in collection.books:
            curbook = Bookdb(parent_collection=curcollect,
                             book_title=book.title,
                             book_author=book.author)
            curbook.save()
            for page in book.pages:

                if page.have_page_image:
                    page_img_path = File(open(page.getfilepath(), "rb"))
                    curpage = Pagedb(page_number=page.number,
                                     parent_book=curbook,
                                     page_image=page_img_path)
                else:
                    curpage = Pagedb(page_number=page.number,
                                     parent_book=curbook)
                curpage.save()

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_title', models.CharField(blank=True, max_length=16)),
                ('book_author', models.CharField(blank=True, max_length=16)),
                ('book_transcriber', models.CharField(blank=True, max_length=16)),
                ('book_notes', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('char_mark', models.CharField(blank=True, max_length=4)),
                ('x1', models.IntegerField(blank=True)),
                ('y1', models.IntegerField(blank=True)),
                ('x2', models.IntegerField(blank=True)),
                ('y2', models.IntegerField(blank=True)),
                ('char_notes', models.TextField(blank=True)),
                ('char_image', models.ImageField(blank=True, storage=django.core.files.storage.FileSystemStorage(location='images'), upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collection_name', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_number', models.IntegerField()),
                ('page_notes', models.TextField(blank=True)),
                ('page_image', models.ImageField(blank=True, storage=django.core.files.storage.FileSystemStorage(location='images'), upload_to='')),
                ('parent_book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calligraphy.Book')),
            ],
        ),
        migrations.AddField(
            model_name='character',
            name='parent_page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calligraphy.Page'),
        ),
        migrations.AddField(
            model_name='book',
            name='parent_collection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calligraphy.Collection'),
        ),
        migrations.RunPython(import_data)
    ]
