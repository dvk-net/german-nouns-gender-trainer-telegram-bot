from django.contrib import admin

from . import models

class WordAdmin(admin.ModelAdmin):
    list_display = ['pk', 'gender', 'word']
    list_editable = ['gender', 'word']

admin.site.register(models.Words, WordAdmin)
