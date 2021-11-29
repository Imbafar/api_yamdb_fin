from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.TextField()
    year = models.SmallIntegerField()
    description = models.TextField(blank=True)
    genre = models.ForeignKey(
        Genres,
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
    )


    def __str__(self):
        return self.name