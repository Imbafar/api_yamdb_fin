from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from .permissions import UserForSelf

from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from reviews.models import Categories, Genres, Titles, User
from .serializers import (CategoriesSerializer,
                          GenresSerializer,
                          TitlesSerializer,
                          UserSerializer)


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

    def get_permissions(self):
        if self.action == 'retrieve' or self.action == 'partial_update':
            return (UserForSelf(),)
        return super().get_permissions()

    def retrieve(self, request, username):
        queryset = User.objects.all()
        if username == 'me':
            user = get_object_or_404(queryset, username=request.user.username)
        user = get_object_or_404(queryset, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, username):
        queryset = User.objects.all()
        if username == 'me':
            user = get_object_or_404(queryset, username=request.user.username)
        user = get_object_or_404(queryset, username=username)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
