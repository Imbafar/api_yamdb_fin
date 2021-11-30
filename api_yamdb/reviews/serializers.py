from rest_framework import serializers

from .models import Categories, Genres, Titles


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('id', 'name', 'slug')


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('id', 'name', 'slug')


class TitlesSerializer(serializers.ModelSerializer):
    genre = GenresSerializer(many=True, required=False)
    # rating = ...

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
