from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage()


class Author(models.Model):
    name = models.CharField(max_length=64)
    dynasty = models.CharField(max_length=64, blank=True)
    def get_absolute_url(self):
        return '/auth/' + str(self.id)


class Work(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=64, blank=True)
    author = models.ForeignKey(Author)
    transcript = models.TextField(blank=True)

    def get_absolute_url(self):
        return '/work/' + str(self.id)


class Page(models.Model):
    book_id = models.IntegerField(null=True)
    page_id = models.IntegerField(null=True)
    image = models.ImageField(blank=True, storage=fs)
    image_width = models.IntegerField(null=True)
    image_length = models.IntegerField(null=True)
    parent_work = models.ForeignKey(Work, null=True)
    transcript = models.TextField(blank=True)
    transform_type = models.CharField(max_length=8, null=True)

    def get_absolute_url(self) -> str:
        return '/page/' + str(self.id)

    def get_image(self) -> str:
        return str(self.image.url)


# Temporary work que classes go here
class ToFindMultiplier(models.Model):
    page_id = models.ForeignKey(Page)
    times_reviewed = models.IntegerField()


class Character(models.Model):
    author_name = models.CharField(max_length=64, blank=True)
    parent_work_name = models.CharField(max_length=64, blank=True)

    parent_page = models.ForeignKey(Page, null=True)
    parent_author = models.ForeignKey(Author, null=True)
    parent_work = models.ForeignKey(Work, null=True)
    mark = models.CharField(max_length=64, blank=True)
    x1 = models.IntegerField(blank=True)
    y1 = models.IntegerField(blank=True)
    x2 = models.IntegerField(blank=True)
    y2 = models.IntegerField(blank=True)
    collection = models.IntegerField(default=0)

    image = models.ImageField(blank=True, storage=fs)
    image_high_rez = models.ImageField(blank=True, storage=fs)
    image_thumb = models.ImageField(blank=True, storage=fs)
    image_thumb_x = models.IntegerField(default=0)
    image_thumb_y = models.IntegerField(default=0)

    def get_absolute_url(self):
        return '/char/' + str(self.id)

    def get_image(self) -> str:
        if self.image_high_rez:
            return str( self.image_high_rez.url)
        
    def get_thumb(self) -> str:
        return str( self.image.url)

    def get_id(self) -> str:
        return '#' + str(self.id)
        
    def get_rel_chars(self):
        return Character.objects.filter(mark=self.mark, parent_author=self.parent_author).exclude(id=self.id)

# Data related to computed offsets goes here.
# Duplication due to need for redundancy between users
class UserSuppliedPageMultiplier(models.Model):
    user_id = models.ForeignKey(User)
    page_id = models.ForeignKey(Page)

class CharSet(models.Model):
    userSupplied = models.ForeignKey(UserSuppliedPageMultiplier)
    set_offset_x = models.FloatField()
    set_offset_y = models.FloatField()
    set_chars = models.ManyToManyField(Character)
    set_has_problems = models.BooleanField()


class RelatedChars(object): # This class exists to hold all chars and related ones
    def __init__(self, inChar: Character):
        self.mainchar = inChar
        self.relatedChars = []
        self.populateRelatedChars(inChar)

    def populateRelatedChars(self, inChar: Character) -> None:
        chars = Character.objects.filter(mark=inChar.mark, author_name=inChar.author_name).exclude(id=inChar.id)
        for char in chars:
            self.relatedChars.append(char)



