from random import randint


from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status

from djangoHW_5_month import settings
from .models import ConfirmCode
from .serializers import UserCreateSerializer, UserAuthSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from rest_framework.views import APIView


class AuthAPIView(APIView):
    def post(self, request):
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)
        if user:
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)
            return Response(data={'key': token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED,
                        data={'error': 'User credentials invalid.'})


class ConfirmCodeAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        code = request.data.get('code')

        try:
            user = User.objects.get(username=username)
            confirm_code = ConfirmCode.objects.get(user=user)

            if confirm_code.code == code:
                user.is_active = True
                user.save()
                confirm_code.delete()
                return Response(status=status.HTTP_200_OK, data={'message': 'Account activated successfully.'})
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Invalid confirmation code.'})
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'User not found.'})
        except ConfirmCode.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'Confirmation code not found.'})


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        email = serializer.validated_data['email']

        user = User.objects.create_user(username=username, password=password, email=email, is_active=False)

        code = str(randint(100000, 999999))

        ConfirmCode.objects.create(user=user, code=code)

        send_mail(
            'Код потверждение',
            f'code: {code}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,

        )

        return Response(status=status.HTTP_201_CREATED,
                        data={"data_id": user.id})