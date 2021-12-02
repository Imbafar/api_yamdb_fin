from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from .permissions import UserForSelf
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import action

import uuid

from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from reviews.models import Categories, Genres, Titles, User
from .serializers import (CategoriesSerializer,
                          GenresSerializer,
                          TitlesSerializer,
                          UserSerializer,
                          AuthSignUpSerializer)


class CreateListViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    pass


class RetrieveUpdateDestroyViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    pass


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer


class AllUsersViewSet(CreateListViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)
    search_fields = ('=username',)


class UserViewSet(RetrieveUpdateDestroyViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)

    @action(detail=True, methods=['GET', 'PATCH'])
    def me(self, request):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=request.user.username)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action == 'retrieve' or self.action == 'partial_update':
            return (UserForSelf(),)
        return super().get_permissions()


def generate_and_send_confirmation_code_to_email(username):
    user = User.objects.get(username=username)
    confirmation_code = str(uuid.uuid3(uuid.NAMESPACE_DNS, username))
    user.confirmation_code = confirmation_code
    send_mail(
        'Код подтвержения для завершения регистрации',
        f'Ваш код для получения JWT токена {confirmation_code}',
        'Wizardus@list.ru',
        ['Elnikit@rambler.ru'],
        fail_silently=False,
    )


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
    pass
    # serializer = AuthCodeSerializer(data=request.data)
    # if serializer.is_valid():
    #     # здесь будет код сравнения к с базой
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
