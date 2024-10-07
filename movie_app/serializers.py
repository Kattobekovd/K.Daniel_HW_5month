from rest_framework import serializers
from movie_app import models


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
    director = DirectorSerializer()
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



