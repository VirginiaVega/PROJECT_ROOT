from django.contrib import admin
from .models import Post, Score
# Register your models here.

class PublicacionAdmin(admin.ModelAdmin):
    list_display=('title', 'body')


admin.site.register(Post, PublicacionAdmin)

class PuntajeAdmin(admin.ModelAdmin):
    list_display = ('score', 'post')  # Mostrar los puntajes y la publicación asociada
    ordering = ('post',)  # Ordenar por la publicación
admin.site.register(Score, PuntajeAdmin)