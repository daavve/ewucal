from django.contrib import admin

from . import models

admin.site.register(models.Collection)
admin.site.register(models.Book)
admin.site.register(models.Page)
admin.site.register(models.Character)
