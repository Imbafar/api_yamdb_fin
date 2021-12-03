from rest_framework import viewsets
from rest_framework import permissions
from .permissions import UserForSelf
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework_simplejwt.tokens import RefreshToken

import uuid

from django.core.mail import send_mail

from reviews.models import Categories, Genres, Titles, User
from .serializers import (CategoriesSerializer,
                          GenresSerializer,
                          TitlesSerializer,
                          UserSerializer,
                          AuthSignUpSerializer,
                          AuthTokenSerializer)


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)
    search_fields = ('=username',)
    lookup_field = 'username'

    @action(detail=False, methods=['GET', 'PATCH'], url_path='me')
    def me(self, request):
        user = User.objects.get(username=request.user.username)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(role=user.role)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action == 'me':
            return (UserForSelf(),)
        return super().get_permissions()


def generate_and_send_confirmation_code_to_email(username):
    user = User.objects.get(username=username)
    confirmation_code = str(uuid.uuid3(uuid.NAMESPACE_DNS, username))
    user.confirmation_code = confirmation_code
    send_mail(
        'Код подтвержения для завершения регистрации',
        f'Ваш код для получения JWT токена {user.confirmation_code}',
        'Wizardus@list.ru',
        ['Elnikit@rambler.ru'],
        fail_silently=False,
    )
    user.save()


@api_view(['POST'])
def signup_new_user(request):
    username = request.data.get('username')
    if not User.objects.filter(username=username).exists():
        serializer = AuthSignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            generate_and_send_confirmation_code_to_email(username)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.get(username=username)
    serializer = AuthSignUpSerializer(
        user, data=request.data, partial=True
    )
    if serializer.is_valid():
        serializer.save()
        generate_and_send_confirmation_code_to_email(username)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_token(request):
    serializer = AuthTokenSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']
        try:
            user = User.objects.get(username=username)
        except Exception:
            return Response(
                'Пользователь не найден', status=status.HTTP_404_NOT_FOUND
            )
        if user.confirmation_code == confirmation_code:
            refresh = RefreshToken.for_user(user)
            token_data = {'token': str(refresh.access_token)}
            return Response(token_data, status=status.HTTP_200_OK)
        return Response(
            'Код подтверждения неверный', status=status.HTTP_400_BAD_REQUEST
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
