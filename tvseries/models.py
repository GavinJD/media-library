from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator


class TVShow(models.Model):
    name = models.CharField(max_length=50)
    media_id = models.CharField(
        max_length=10,
        primary_key=True,
        validators=[
            RegexValidator(
                regex='^TV(\w{8})$', message='media_id for TV season must follow TV[8 digit ID]', code='nomatch')
        ]
    )

    class Meta:
        verbose_name = "TV Show"
        verbose_name_plural = "TV Shows"

    def __str__(self):
        return self.name


class TVSeason(models.Model):
    show = models.ForeignKey('TVShow', on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField(default=1)
    foldername = models.CharField(max_length=50)

    class Meta:
        verbose_name = "TV Season"
        verbose_name_plural = "TV Seasons"
        constraints = [
            models.UniqueConstraint(
                fields=['show', 'number'],
                name='No repeating tv seasons'
            )
        ]

#     def __str__(self):
#         return self.name


class TVEpisode(models.Model):
    season = models.ForeignKey('TVSeason', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    urlPath = models.URLField()

    class Meta:
        verbose_name = "TV Episode"
        verbose_name_plural = "TV Episodes"
        constraints = [
            models.UniqueConstraint(
                fields=['season', 'name'],
                name='No repeating tv season episodes'
            )
        ]

    def __str__(self):
        return self.name


class TVMetadata(models.Model):
    media = models.OneToOneField(
        'TVShow',
        on_delete=models.CASCADE,
        primary_key=True
    )
    poster = models.URLField()
    year = models.IntegerField(
        default=2000,
        validators=[
            MinValueValidator(1850),
            MaxValueValidator(2100)
        ]
    )
    description = models.TextField(default='Default TV Show Description')
    rating = models.DecimalField(max_digits=2, decimal_places=1)

    class Meta:
        verbose_name = "TV Metadata"
        verbose_name_plural = "TV Metadata"


class Genre(models.Model):
    genre_id = models.IntegerField(primary_key=True)
    genre = models.CharField(max_length=40)

    class Meta:
        verbose_name = "TV Genre"
        verbose_name_plural = "TV Genres"

    def __str__(self):
        return self.genre


class TVGenre(models.Model):
    media = models.ForeignKey('TVShow', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['media', 'genre'], name='No repeating tv genres')
        ]

class TVPlayHistory(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    media = models.ForeignKey('TVShow', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
