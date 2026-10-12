from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("favorite/<int:song_id>/", views.toggle_favorite, name="toggle_favorite"),
    path("register/", views.register, name="register"),
    path("login/", LoginView.as_view(template_name="yo/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("playlists/", views.playlist_list, name="playlist_list"),
    path("playlists/create/", views.playlist_create, name="playlist_create"),
    path("playlists/<int:pk>/", views.playlist_detail, name="playlist_detail"),
    path("playlists/<int:playlist_id>/add/<int:song_id>/", views.add_to_playlist, name="add_to_playlist"),
]