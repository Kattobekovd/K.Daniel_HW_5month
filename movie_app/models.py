from django.db import models


class Director(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField()
    director = models.ForeignKey(Director, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return self.title


STARS = (
    (1, '⭐'),
    (2, '⭐ ⭐'),
    (3, '⭐ ⭐ ⭐'),
    (4, '⭐ ⭐ ⭐ ⭐'),
    (5, '⭐ ⭐ ⭐ ⭐ ⭐'),
)


class Review(models.Model):
    text = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')

    stars = models.IntegerField(choices=STARS, default=5)

    def __str__(self):
        return self.text


