import uuid

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Categories, Comments, Genres, Review, Title, User

from .permissions import (AdminOrReadOnly, IsAdminOrStaffPermission,
                          IsAuthorOrModerPermission, IsUserForSelfPermission)
from .serializers import (AuthSignUpSerializer, AuthTokenSerializer,
                          CategoriesSerializer, CommentsSerializer,
                          GenresSerializer, ReviewSerializer, TitlesSerializer,
                          UserSerializer)


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class CategoriesViewSet(CreateListDestroyViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)


class GenresViewSet(CreateListDestroyViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitlesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrModerPermission]

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        new_queryset = Review.objects.filter(title=title)
        return new_queryset


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrModerPermission]

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title)
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title)
        new_queryset = Comments.objects.filter(review=review)
        return new_queryset


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrStaffPermission,)
    search_fields = ('=username',)
    lookup_field = 'username'

    @action(detail=False, methods=['GET', 'PATCH', 'DELETE'])
    def me(self, request):
        if request.method == 'DELETE':
            return Response(
                {"detail": "Method \"DELETE\" not allowed."},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
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
            return (IsUserForSelfPermission(),)
        return super().get_permissions()


def generate_and_send_confirmation_code_to_email(username):
    user = User.objects.get(username=username)
    confirmation_code = str(uuid.uuid3(uuid.NAMESPACE_DNS, username))
    user.confirmation_code = confirmation_code
    send_mail(
        'Код подтвержения для завершения регистрации',
        f'Ваш код для получения JWT токена {user.confirmation_code}',
        'Wizardus@list.ru',
        [user.email],
        fail_silently=False,
    )
    user.save()


@api_view(['POST'])
def signup_new_user(request):
    username = request.data.get('username')
    if not User.objects.filter(username=username).exists():
        serializer = AuthSignUpSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['username'] != 'me':
                serializer.save()
                generate_and_send_confirmation_code_to_email(username)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                'Username указан невено!', status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.get(username=username)
    serializer = AuthSignUpSerializer(
        user, data=request.data, partial=True
    )
    if serializer.is_valid():
        if serializer.validated_data['email'] == user.email:
            serializer.save()
            generate_and_send_confirmation_code_to_email(username)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            'Почта указана неверно!', status=status.HTTP_400_BAD_REQUEST
        )
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
