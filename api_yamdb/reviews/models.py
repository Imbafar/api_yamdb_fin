from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Админ'),
)


class Custom_User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    role = models.CharField(
        max_length=16, choices=CHOICES, default='user'
    )
    bio = models.TextField(blank=True)
    confirmation_code = models.CharField(max_length=50, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]


User = get_user_model()


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


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.SmallIntegerField()
    # rating = models.SmallIntegerField()
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(
        Genres,
        # blank=True,
        db_index=True
        # through='GenresTitles',
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


# class GenresTitles(models.Model):
#     genre = models.ForeignKey(Genres, on_delete=models.CASCADE)
#     title = models.ForeignKey(Titles, on_delete=models.CASCADE)

#     def __str__(self):
#         return f'{self.genre} {self.title}'


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    score = models.IntegerField()
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_review'
            )
        ]

    def __str__(self):
        return self.text[:15]


class Comments(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text[:15]
