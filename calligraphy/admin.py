from django.contrib import admin

from .models import Collection, Book, Page, Character

admin.site.register(Collection)
admin.site.register(Book)
admin.site.register(Page)
admin.site.register(Character)
