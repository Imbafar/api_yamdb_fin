import datetime as dt

from rest_framework import serializers
from reviews.models import (Categories, Comments, Genres, GenresTitles, Review,
                            Titles, User)


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('name', 'slug')


class GenresSlugSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('slug',)


class TitlesSerializer(serializers.ModelSerializer):
    genre = GenresSlugSerializer(many=True, required=True)
    # rating = ...

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Titles.objects.create(**validated_data)
        for genre in genres:
            current_genre, status = Genres.objects.get_or_create(
                **genre)
            GenresTitles.objects.create(
                genre=current_genre, title=title)
        return title

    def validate_year(self, value):
        year = dt.date.today().year
        if not (0 < value <= year):
            raise serializers.ValidationError('Проверьте год произведения!')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        model = Review

    def validate(self, data):
        if not 1 <= data['score'] <= 10:
            raise serializers.ValidationError(
                'Оценка может быть от 1 до 10!')
        return data


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date',)
        model = Comments


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class AuthSignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=50)
