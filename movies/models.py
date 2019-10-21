from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator


class Movie(models.Model):
    name = models.CharField(max_length=50)
    media_id = models.CharField(
        max_length=10,
        primary_key=True,
        validators=[
            RegexValidator(
                regex='^MV(\w{8})$', message='media_id for movie must follow MV[8 digit ID]', code='nomatch')
        ]
    )
    urlPath = models.URLField()

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"

    def __str__(self):
        return self.name

class MovieMetadata(models.Model):
    media_id = models.OneToOneField('Movie', on_delete=models.CASCADE)
    director = models.CharField(max_length=50)
    poster = models.URLField()
    year = models.IntegerField(
        default=2000,
        validators=[
            MinValueValidator(1850),
            MaxValueValidator(2100)
        ]
    )
    description = models.TextField(default='Default Movie Description')
    rating = models.DecimalField(max_digits=2, decimal_places=1)

    class Meta:
        verbose_name = "Movie Metadata"
        verbose_name_plural = "Movie Metadata"

    def __str__(self):
        return f'{Movie.objects.get(media_id=self.media_id_id).name} metadata'
        

class Genre(models.Model):
    genre_id = models.IntegerField(primary_key=True)
    genre = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Movie Genre"
        verbose_name_plural = "Movie Genres"
    
    def __str__(self):
        return self.genre

class MovieGenre(models.Model):
    media = models.ForeignKey('Movie', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)

    def __str__(self):
        return f'{Movie.objects.get(media_id=self.media_id)} - {Genre.objects.get(genre_id=self.genre_id)}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['media', 'genre'], name='No repeating genres')
        ]
