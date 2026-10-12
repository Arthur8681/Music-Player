from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from .models import Genre, Playlist, Song


def index(request):
    query = request.GET.get("q", "")
    genre_id = request.GET.get("genre", "")
    filter_type = request.GET.get("filter", "")

    songs = Song.objects.all().order_by("-uploaded_at")

    if query:
        songs = songs.filter(title__icontains=query) | songs.filter(
            artist__icontains=query
        )

    if genre_id:
        songs = songs.filter(genre_id=genre_id)

    if filter_type == "favorites" and request.user.is_authenticated:
        songs = songs.filter(favorited_by=request.user)

    genres = Genre.objects.all()
    user_playlists = (
        request.user.playlists.all() if request.user.is_authenticated else []
    )

    return render(
        request,
        "yo/index.html",
        {
            "songs": songs,
            "genres": genres,
            "selected_genre": genre_id,
            "query": query,
            "filter_type": filter_type,
            "user_playlists": user_playlists,
        },
    )


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = UserCreationForm()
    return render(request, "yo/register.html", {"form": form})


def toggle_favorite(request, song_id):
    if not request.user.is_authenticated:
        return redirect("login")
    song = get_object_or_404(Song, id=song_id)
    if song.favorited_by.filter(id=request.user.id).exists():
        song.favorited_by.remove(request.user)
    else:
        song.favorited_by.add(request.user)
    return redirect(request.META.get("HTTP_REFERER", "index"))


def playlist_list(request):
    if not request.user.is_authenticated:
        return redirect("login")
    playlists = request.user.playlists.all()
    return render(request, "yo/playlist_list.html", {"playlists": playlists})


def playlist_create(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Playlist.objects.create(name=name, user=request.user)
            return redirect("playlist_list")
    return render(request, "yo/playlist_create.html")


def playlist_detail(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk, user=request.user)
    return render(request, "yo/playlist_detail.html", {"playlist": playlist})


def add_to_playlist(request, playlist_id, song_id):
    if not request.user.is_authenticated:
        return redirect("login")
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    song = get_object_or_404(Song, id=song_id)
    playlist.songs.add(song)
    return redirect(request.META.get("HTTP_REFERER", "index"))