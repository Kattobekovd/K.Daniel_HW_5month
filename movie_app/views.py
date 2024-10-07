from rest_framework.decorators import api_view
from rest_framework.response import Response
from movie_app import models
from movie_app.serializers import DirectorSerializer, MovieSerializer, ReviewSerializer
from rest_framework import status


#Вывод списка именами всех режисерев
@api_view(http_method_names=['GET'])
def director_list_api_view(request):
    post = models.Director.objects.all()

    data = DirectorSerializer(instance=post, many=True).data
    return Response(data=data)


#Вывод имена режисерев по ID
@api_view(http_method_names=['GET'])
def director_detail_api_view(request, id):
    try:
        post1 = models.Director.objects.get(id=id)
    except models.Director.DoesNotExist:
        return Response(data={'error': 'Post not found'},
                        status=status.HTTP_404_NOT_FOUND)

    data = DirectorSerializer(instance=post1, many=False).data
    return Response(data=data)


#Здесь получаем список всех фильмов
@api_view(http_method_names=['GET'])
def movie_list_api_view(request):
    movies = models.Movie.objects.all()

    data = MovieSerializer(instance=movies, many=True).data
    return Response(data=data)


#Вывод фильмов по ID
@api_view(http_method_names=['GET'])
def movie_detail_api_view(request, id):
    try:
        movie = models.Movie.objects.get(id=id)
    except models.Movie.DoesNotExist:
        return Response(data={'error': 'Post not found'},
                        status=status.HTTP_404_NOT_FOUND)

    data = MovieSerializer(instance=movie, many=False).data
    return Response(data=data)


#Вывод листа всех коментариев
@api_view(http_method_names=['GET'])
def review_list_api_view(request):
    reviews = models.Review.objects.all()
    data = ReviewSerializer(instance=reviews, many=True).data
    return Response(data=data)


#Выводим коментарии исключительно по ID
@api_view(http_method_names=['GET'])
def review_detail_api_view(request, id):
    try:
        review = models.Review.objects.get(id=id)
    except models.Review.DoesNotExist:
        return Response(data={'error': 'Post not found'},
                        status=status.HTTP_404_NOT_FOUND)

    data = ReviewSerializer(instance=review, many=False).data
    return Response(data=data)


@api_view(http_method_names=['GET'])
def movie_review_list_api_view(request):
    reviews = models.Movie.objects.prefetch_related('reviews')
    data = MovieSerializer(instance=reviews, many=True).data
    return Response(data=data)
