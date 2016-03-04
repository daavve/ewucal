from django.contrib import admin

from . import models


class CAuthor(admin.ModelAdmin):
    list_display = ('id', 'name', 'dynasty')
    list_filter = ['dynasty']
    search_fields = ['name']


class CWork(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'transcript')
    search_fields = ['title', 'transcript']


class CPage(admin.ModelAdmin):
    list_display = ('id', 'image', 'transcript')
    search_fields = ['transcript']


class CCharacter(admin.ModelAdmin):
    list_display = ('id', 'mark', 'x1', 'y1', 'x2', 'y2', 'image')
    search_fields = ['mark']

admin.site.register(models.Author, CAuthor)
admin.site.register(models.Work, CWork)
admin.site.register(models.Page, CPage)
admin.site.register(models.Character, CCharacter)
