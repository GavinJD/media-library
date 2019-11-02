from django.urls import path
from .views import FolderAddView, MovieListView, MovieDetailView, VideoPlayerView
from .views import addFolder, playVideo

app_name = 'movies'
urlpatterns = [
    path("", MovieListView.as_view(), name="movie_list"),
    path("addFTP/", FolderAddView.as_view(), name="addFTP"),
    path("ajax/addFTP/", addFolder, name="ajax_addFTP"),
    path("<pk>/", MovieDetailView.as_view(), name="movie_detail"),
    path("play/<path:urlPath>", playVideo, name="playVideo"),
    path("playing/<path:urlPath>", VideoPlayerView.as_view(), name="video_player"),
]
