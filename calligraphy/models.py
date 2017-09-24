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
    has_copyright_restrictions = models.BooleanField(default=False)
    image_works = models.BooleanField(default=True)

    def get_absolute_url(self) -> str:
        return '/page/' + str(self.id)

    def get_image(self) -> str:
        return str(self.image)


class FlagForReview(models.Model):
    flagged_by = models.ForeignKey(User)
    parent_page = models.ForeignKey(Page)
    
# Integer Max: 2147483647

class DetectedBox(models.Model):
    inside_currated_box = models.BooleanField()  # True if overlap rating is > 80%
    inside_orig_box = models.BooleanField()      # True if overlap rating is > 80%
    parent_page = models.ForeignKey(Page)
    black_chars = models.BooleanField() 
    area_norm = models.IntegerField()
    #convex_area_norm = models.IntegerField()   #don't think it's important because it correlates so strongly with area_norm
    eccentricity_norm = models.IntegerField()
    #extant_norm = models.IntegerField()        #TODO: Accedentally set to zero a while ago Go back and recover it.
    x1 = models.IntegerField()
    y1 = models.IntegerField()
    x2 = models.IntegerField()
    y2 = models.IntegerField()
    major_axis_length_norm = models.IntegerField()
    minor_axis_length_norm = models.IntegerField()
    orientation_norm = models.IntegerField()
    solidity_norm = models.IntegerField()
    local_centroid_x_norm = models.IntegerField()
    local_centroid_y_norm = models.IntegerField()
    li_threshold_bottom_norm = models.IntegerField()
    li_threshold_top_norm = models.IntegerField()




class Character_orig(models.Model):
    author_name = models.CharField(max_length=64, blank=True)
    parent_work_name = models.CharField(max_length=64, blank=True)
    
    supplied_by = models.ForeignKey(User)

    parent_page = models.ForeignKey(Page, null=True)
    parent_author = models.ForeignKey(Author, null=True)
    parent_work = models.ForeignKey(Work, null=True)
    mark = models.CharField(max_length=64, blank=True)
    x1 = models.IntegerField(blank=True)
    y1 = models.IntegerField(blank=True)
    x2 = models.IntegerField(blank=True)
    y2 = models.IntegerField(blank=True)

    image = models.ImageField(blank=True, storage=fs)
    image_width = models.IntegerField(default=0)
    image_height = models.IntegerField(default=0)


class Character(models.Model):
    author_name = models.CharField(max_length=64, blank=True)
    parent_work_name = models.CharField(max_length=64, blank=True)
    
    supplied_by = models.ForeignKey(User)

    parent_page = models.ForeignKey(Page, null=True)
    parent_author = models.ForeignKey(Author, null=True)
    parent_work = models.ForeignKey(Work, null=True)
    mark = models.CharField(max_length=64, blank=True)
    x1 = models.IntegerField(blank=True)
    y1 = models.IntegerField(blank=True)
    x2 = models.IntegerField(blank=True)
    y2 = models.IntegerField(blank=True)

    image = models.ImageField(blank=True, storage=fs)
    image_width = models.IntegerField(default=0)
    image_height = models.IntegerField(default=0)
    
    deleted = models.BooleanField(default=False)
    
    def get_absolute_url(self):
        return '/char/' + str(self.id)

    def get_image(self) -> str:
            return str( self.image)

    def get_thumb(self) -> str:
        return str( self.image.url)

    def get_id(self) -> str:
        return '#' + str(self.id)

    def get_rel_chars(self):
        return Character.objects.filter(mark=self.mark, parent_author=self.parent_author).exclude(id=self.id)
        
class ReasonCharDeleted(models.Model):
    user_deleted = models.ForeignKey(User)
    target_char = models.ForeignKey(Character)
    reason_deleted = models.CharField(max_length=64, blank=False)

# Data related to computed offsets goes here.
class UserSuppliedPageMultiplier(models.Model):
    user_id = models.ForeignKey(User)
    page_id = models.ForeignKey(Page)
    image_rotation = models.IntegerField()

class TodoScanned(models.Model):
    toCheck = models.ForeignKey(Page)

class ToDrawBoxesWBoxes(models.Model):
    toCheck = models.ForeignKey(Page)

class ToDrawBoxesWoBoxes(models.Model):
    toCheck = models.ForeignKey(Page)

class PagesHaveChars(models.Model):
    haveChars = models.ForeignKey(Page)
    x1 = models.IntegerField()       # Perhaps Create it's own object so we can have multiple areas of interest within an image
    x2 = models.IntegerField()
    y1 = models.IntegerField()
    y2 = models.IntegerField()

class CharSet(models.Model):
    userSupplied = models.ForeignKey(UserSuppliedPageMultiplier)
    set_offset_x = models.FloatField()
    set_offset_y = models.FloatField()
    set_chars_orig = models.ManyToManyField(Character_orig)
    set_valid = models.BooleanField()

class UserDid(models.Model):
    user_supplied = models.ForeignKey(User)
    pages_changed = models.ManyToManyField(Page)
    chars_changed = models.ManyToManyField(Character)


class RelatedChars(object): # This class exists to hold all chars and related ones
    def __init__(self, inChar: Character):
        self.mainchar = inChar
        self.relatedChars = []
        self.populateRelatedChars(inChar)

    def populateRelatedChars(self, inChar: Character) -> None:
        chars = Character.objects.filter(mark=inChar.mark, author_name=inChar.author_name).exclude(id=inChar.id)
        for char in chars:
            self.relatedChars.append(char)



