from django.urls import path
from .views import TvListView, TvDetailView, addFolder, FolderAddView, playVideo, VideoPlayerView

app_name = 'tvseries'
urlpatterns = [
    path("", TvListView.as_view(), name="tv_list"),
    path("addFTP/", FolderAddView.as_view(), name="addFTP"),
    path("ajax/addFTP", addFolder, name="ajax_addFTP"),
    path("<pk>/", TvDetailView.as_view(), name="tv_detail"),
    path("play/<path:urlPath>", playVideo, name="playVideo"),
    path("playing/<path:urlPath>", VideoPlayerView.as_view(), name="video_player"),
]
