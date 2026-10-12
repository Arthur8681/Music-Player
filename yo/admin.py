from django.contrib import admin
from .models import Genre, Playlist, Song

admin.site.register(Song)
admin.site.register(Genre)
admin.site.register(Playlist)