from rest_framework.decorators import api_view
from rest_framework.response import Response
from movie_app import models
from movie_app.serializers import DirectorSerializer, MovieSerializer, ReviewSerializer, DirectorValidateSerializer, MovieValidateSerializer, ReviewValidateSerializer
from rest_framework import status


#Вывод списка именами всех режисерев
@api_view(http_method_names=['GET', 'POST'])
def director_list_create_api_view(request):
    if request.method == 'GET':
        post = models.Director.objects.all()

        data = DirectorSerializer(instance=post, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
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


#Вывод имена режисерев по ID
@api_view(http_method_names=['GET', 'PUT', 'DELETE'])
def director_detail_api_view(request, id):
    try:
        post1 = models.Director.objects.get(id=id)
    except models.Director.DoesNotExist:
        return Response(data={'error': 'Post not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = DirectorSerializer(instance=post1, many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = DirectorValidateSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data=serializer.errors)
        post1.name = serializer.validated_data.get('name')
        post1.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=DirectorSerializer(post1).data)
    elif request.method == 'DELETE':
        post1.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#Здесь получаем список всех фильмов
@api_view(http_method_names=['GET', 'POST'])
def movie_list_create_api_view(request):
    if request.method == 'GET':
        movies = models.Movie.objects.all()

        data = MovieSerializer(instance=movies, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
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


#Вывод фильмов по ID
@api_view(http_method_names=['GET', 'PUT', 'DELETE'])
def movie_detail_api_view(request, id):
    try:
        movie = models.Movie.objects.get(id=id)
    except models.Movie.DoesNotExist:
        return Response(data={'error': 'Post not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = MovieSerializer(instance=movie, many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = MovieValidateSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data=serializer.errors)
        movie.title = serializer.validated_data.get('title')
        movie.description = serializer.validated_data.get('description')
        movie.duration = serializer.validated_data.get('duration')
        movie.director_id = serializer.validated_data.get('director_id')
        movie.save()
        return Response(status=status.HTTP_201_CREATED,
                        data={'movie_id': movie.id})
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#Вывод листа всех коментариев
@api_view(http_method_names=['GET','POST'])
def review_list_create_api_view(request):
    if request.method == 'GET':
        reviews = models.Review.objects.all()
        data = ReviewSerializer(instance=reviews, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
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


#Выводим коментарии исключительно по ID
@api_view(http_method_names=['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = models.Review.objects.get(id=id)
    except models.Review.DoesNotExist:
        return Response(data={'error': 'Post not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ReviewSerializer(instance=review, many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data=serializer.errors)
        review.text = serializer.validated_data.get('text')
        review.movie_id = serializer.validated_data.get('movie_id')
        review.stars = serializer.validated_data.get('stars')
        review.save()
        return Response(status=status.HTTP_201_CREATED,
                        data={'review_id': review.id})
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['GET'])
def movie_review_list_api_view(request):
    reviews = models.Movie.objects.prefetch_related('reviews')
    data = MovieSerializer(instance=reviews, many=True).data
    return Response(data=data)
