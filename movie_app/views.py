from rest_framework.response import Response
from movie_app import models
from movie_app.models import Director, Movie, Review
from movie_app.serializers import DirectorSerializer, MovieSerializer, ReviewSerializer, DirectorValidateSerializer, MovieValidateSerializer, ReviewValidateSerializer
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView



class DirectorListAPIView(ListCreateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

    def post(self, request, *args, **kwargs):
        serializer = DirectorValidateSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data=serializer.errors)
        name = request.data.get('name')
        director = models.Director.objects.create(
            name=name
        )
        return Response(status=status.HTTP_201_CREATED,
                        data={'director_id': director.id})


class DirectorDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    lookup_field = 'id'


class MovieListAPIView(ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def post(self, request, *args, **kwargs):
        serializer = MovieValidateSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data=serializer.errors)
        title = request.data.get('title')
        description = request.data.get('description')
        duration = request.data.get('duration')
        director_id = request.data.get('director_id')

        movie = models.Movie.objects.create(
            title=title,
            description=description,
            duration=duration,
            director_id=director_id
        )
        return Response(status=status.HTTP_201_CREATED,
                        data={'movie_id': movie.id})


class MovieDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'id'


class ReviewListAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def post(self, request, *args, **kwargs):
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data=serializer.errors)
        text = request.data.get('text')
        movie_id = request.data.get('movie_id')
        stars = request.data.get('stars')
        review = models.Review.objects.create(
            movie_id=movie_id,
            text=text,
            stars=stars
        )
        return Response(status=status.HTTP_201_CREATED,
                        data={'review_id': review.id})


class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'


class MovieReviewListAPIView(ListCreateAPIView):
    queryset = Movie.objects.prefetch_related('reviews')
    serializer_class = MovieSerializer

