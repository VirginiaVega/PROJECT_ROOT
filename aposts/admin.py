from django.contrib import admin
from .models import Post, Score
# Register your models here.

class PublicacionAdmin(admin.ModelAdmin):
    list_display=('title', 'body')

admin.site.register(Post, PublicacionAdmin)

class PuntajeAdmin(admin.ModelAdmin):
    list_display = ('score', 'post') 
    ordering = ('post',) 
admin.site.register(Score, PuntajeAdmin)