from django.contrib.auth.models import User
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL, null=True, blank=True
    )
    audio_file = models.FileField(upload_to="songs/")
    cover = models.ImageField(upload_to="covers/", blank=True, null=True)
    favorited_by = models.ManyToManyField(
        User, related_name="favorites", blank=True
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} — {self.artist}"


class Playlist(models.Model):
    name = models.CharField(max_length=150)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="playlists"
    )
    songs = models.ManyToManyField(Song, related_name="playlists", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"