from django.contrib import admin

from .models import Book, Page, Character

admin.site.register(Book)
admin.site.register(Page)
admin.site.register(Character)
