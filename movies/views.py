import movies.addDirFTP
import movies.tmdbCaller
import subprocess
import time

from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from .models import (
    Movie,
    MovieMetadata,
    Genre,
    MovieGenre,
    PlayHistory
)


class FolderAddView(TemplateView):
    template_name = 'folderAddMovie.html'


class MovieListView(ListView):
    model = Movie
    template_name = 'movie_list.html'
    context_object_name = 'movie_list'

    def get_context_data(self, **kwargs):
        context = {}
        context[self.context_object_name] = Movie.objects.extra(
            select={'poster': 'SELECT movies_moviemetadata.poster FROM movies_moviemetadata where movies_moviemetadata.media_id = movies_movie.media_id'}
        )
        return context


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movie_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['metadata'] = MovieMetadata.objects.get(pk=self.kwargs['pk'])
        gList = []
        for g in MovieGenre.objects.filter(media_id=self.kwargs['pk']).select_related('genre'):
            gList.append(g.genre.genre)
        context['genres'] = ', '.join(gList)
        return context


def playVideo(request, urlPath):
    mediaid = request.GET.get('movieid')
    m = Movie.objects.get(pk=mediaid)
    url = urlPath
    p = PlayHistory(
        media=m,
        user=request.user,
    )
    p.save()
    return redirect('movies:video_player', urlPath=url)

class VideoPlayerView(TemplateView):
    template_name = 'movievideoplayer.html'


def addFolder(request):
    if request.method == 'POST':
        address = request.POST.get('ip_address')
        port = int(request.POST.get('port'))
        response = {}

        movieList = movies.addDirFTP.getData(address, port)
        response['found'] = movieList

        metadataList = movies.tmdbCaller.getMetadataList(movieList)
        response['added'] = []
        for item in metadataList:
            m = Movie(
                name=item['Name'],
                media_id=item['MediaID'],
                urlPath='ftp://' + str(address) + ':' +
                str(port) + '/' + item['Url']
            )
            m.save()
            md = MovieMetadata(
                media=m,
                director='',
                poster=item['Poster'],
                year=item['Year'],
                description=item['Description'],
                rating=item['Rating']
            )
            md.save()
            for gid in item['Genres']:
                g = Genre.objects.get(pk=gid)
                mg = MovieGenre(
                    media=m,
                    genre=g
                )
                mg.save()
            response['added'].append(item['Name'])
        # return JsonResponse(response)
        return redirect('movies:movie_list')
