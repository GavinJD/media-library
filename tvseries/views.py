import tvseries.addDirFTP
import tvseries.tmdbCaller

from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.http import Http404
from .models import (
    TVShow,
    TVMetadata,
    TVSeason,
    TVEpisode,
    Genre,
    TVGenre,
    TVPlayHistory
)


class TvListView(ListView):
    template_name = "tv_list.html"
    model = TVShow
    context_object_name = "tv_list"

    def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        context = {}
        context[self.context_object_name] = TVShow.objects.extra(
            select={'poster': 'SELECT tvseries_tvmetadata.poster FROM tvseries_tvmetadata where tvseries_tvmetadata.media_id = tvseries_tvshow.media_id'}
        )
        return context


class TvDetailView(DetailView):
    template_name = "tv_detail.html"
    model = TVShow

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['metadata'] = TVMetadata.objects.get(pk=self.kwargs['pk'])
        context['seasons'] = TVSeason.objects.filter(show=self.kwargs['pk'])
        context['episodes'] = TVEpisode.objects.filter(
            season=context['seasons'][0].pk)
        for s in context['seasons']:
            context['episodes'] = context['episodes'] | TVEpisode.objects.filter(
                season=s.pk)
        return context


class FolderAddView(TemplateView):
    template_name = 'folderAddTV.html'

def addFolder(request):
    if(request.method == 'POST'):
        ip_address = request.POST.get('ip_address')
        port = int(request.POST.get('port'))

        tvList = tvseries.addDirFTP.getData(ip_address, port)
        tvList = tvseries.tmdbCaller.getMetadataList(tvList)

        for show in tvList:
            base_url = 'ftp://' + str(ip_address) + ':' + str(port) \
                + '/' + 'TV Shows' + '/' + show[0] + '/'
            tv = TVShow(
                name=show[0],
                media_id=show[1]['MediaID']
            )
            tv.save()
            tvmeta = TVMetadata(
                media=tv,
                poster=show[1]['Poster'],
                year=show[1]['Year'],
                description=show[1]['Description'],
                rating=show[1]['Rating']
            )
            tvmeta.save()
            for gid in show[1]['Genres']:
                g = Genre.objects.get(pk=gid)
                tg = TVGenre(
                    media=tv,
                    genre=g
                )
                tg.save()
            n = 1
            for season in show[2]:
                season_base_url = base_url + season[0] + '/'
                tvseason = TVSeason(
                    show=tv,
                    number=n,
                    foldername=season[0]
                )
                tvseason.save()
                n += 1
                for episode in season[1]:
                    ep = TVEpisode(
                        season=tvseason,
                        name=episode,
                        urlPath=season_base_url + str(episode)
                    )
                    ep.save()
        return redirect('tvseries:tv_list')
    else:
        return Http404

def playVideo(request, urlPath):
    mediaid = request.GET.get('tvid')
    t = TVShow.objects.get(pk=mediaid)
    url = urlPath
    p = TVPlayHistory(
        media=t,
        user=request.user,
    )
    p.save()
    return redirect('tvseries:video_player', urlPath=url)

class VideoPlayerView(TemplateView):
    template_name = 'tvvideoplayer.html'
