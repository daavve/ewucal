from django.contrib import admin

from . import models


class CollectionAdmin(admin.ModelAdmin):
    list_display = ('collection_name', 'id')


class CollectionBook(admin.ModelAdmin):
    list_display = ('book_title', 'book_author')


class CollectionPage(admin.ModelAdmin):
    list_display = ('page_number', 'page_image')


class CollectionCharacter(admin.ModelAdmin):
    list_display = ('char_mark', 'x1', 'y1', 'x2', 'y2', 'char_image')

admin.site.register(models.Collection, CollectionAdmin)
admin.site.register(models.Book, CollectionBook)
admin.site.register(models.Page, CollectionPage)
admin.site.register(models.Character, CollectionCharacter)
