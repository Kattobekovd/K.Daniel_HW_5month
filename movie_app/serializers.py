from rest_framework import serializers
from movie_app import models
from rest_framework.exceptions import ValidationError

from movie_app.models import Director


class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Director
        fields = 'id name movies_count'.split()

    def get_movies_count(self, obj):
        return obj.movie_set.count()


class ReviewSerializer(serializers.ModelSerializer):
    movie_name = serializers.SerializerMethodField()
    stars_emoji = serializers.SerializerMethodField()

    class Meta:
        model = models.Review
        fields = 'id text movie_name stars_emoji '.split()
        depth = 1

    def get_movie_name(self, post):
        return post.movie.title if post.movie else None

    def get_stars_emoji(self, obj):
        # Создаем словарь соответствия чисел и эмодзи
        stars_mapping = {
            1: '⭐',
            2: '⭐ ⭐',
            3: '⭐ ⭐ ⭐',
            4: '⭐ ⭐ ⭐ ⭐',
            5: '⭐ ⭐ ⭐ ⭐ ⭐',
        }
        return stars_mapping.get(obj.stars, '')


class MovieSerializer(serializers.ModelSerializer):
    director = DirectorSerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = models.Movie
        fields = 'id title description duration director reviews average_rating'.split()

    def get_average_rating(self, post):
        if not post.reviews.exists():
            return 0

        total_stars = sum(review.stars for review in post.reviews.all())
        average_rating = total_stars / post.reviews.count()
        return average_rating


class DirectorValidateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=5, max_length=250)


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(min_length=5, max_length=250)
    movie_id = serializers.IntegerField(min_value=0, max_value=100)
    stars = serializers.IntegerField(min_value=1, max_value=5)

    def validate_movie_id(self, movie_id):
        try:
            models.Movie.objects.get(id=movie_id)
        except models.Movie.DoesNotExist:
            raise ValidationError('Movie does not exist')
        return movie_id


class MovieValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=5, max_length=250)
    description = serializers.CharField(min_length=5, max_length=300)
    duration = serializers.IntegerField(min_value=0, max_value=1000)
    director_id = serializers.IntegerField(min_value=1)

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            raise ValidationError('Director does not exist!')
        return director_id




