import datetime as dt

from rest_framework import serializers

from reviews.models import Categories, Genres, GenresTitles, Titles


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('id', 'name', 'slug')


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('id', 'name', 'slug')


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
