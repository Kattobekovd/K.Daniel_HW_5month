from rest_framework import serializers
from movie_app import models


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Director
        fields = 'id name'.split()


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Movie
        fields = 'id title description duration director'.split()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = 'id text movie'.split()