from django.core.management.base import BaseCommand
import csv
from reviews.models import Categories, Comments, Genres, Review, Title, User

paths = (
    '/Users/NikitaChalykh/Dev/api_yamdb/api_yamdb/static/data/category.csv',
    '/Users/NikitaChalykh/Dev/api_yamdb/api_yamdb/static/data/comments.csv',
    '/Users/NikitaChalykh/Dev/api_yamdb/api_yamdb/static/data/genre_title.csv',
    '/Users/NikitaChalykh/Dev/api_yamdb/api_yamdb/static/data/genre.csv',
    '/Users/NikitaChalykh/Dev/api_yamdb/api_yamdb/static/data/review.csv',
    '/Users/NikitaChalykh/Dev/api_yamdb/api_yamdb/static/data/titles.csv',
    '/Users/NikitaChalykh/Dev/api_yamdb/api_yamdb/static/data/users.csv'
)


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        # with open(paths[6]) as f:
        #     reader = csv.reader(f)
        #     for row in reader:
        #         _, created = User.objects.get_or_create(
        #             username=row[1],
        #             email=row[2],
        #             role=row[1],
        #             bio=row[2],
        #             first_name=row[1],
        #             last_name=row[2]
        #         )
        #     print('User is imported')
        with open(paths[0]) as f:
            reader = csv.reader(f)
            for row in reader:
                _, created = Categories.objects.get_or_create(
                    id=int(row[0]),
                    name=row[1],
                    slug=row[2]
                )
            print('Categories is imported')
        # with open(paths[1]) as f:
        #     reader = csv.reader(f)
        #     for row in reader:
        #         _, created = Comments.objects.get_or_create(
        #             id=int(float(row[0])),
        #             review_id=row[1],
        #             text=row[2],
        #             author=row[3],
        #             pub_date=row[2]
        #         )
        #     print('Comments is imported')
        # with open(paths[2]) as f:
        #     reader = csv.reader(f)
        #     for row in reader:
        #         _, created = Genres.objects.get_or_create(
        #             name=row[1],
        #             slug=row[2]
        #         )
        #     print('Genres is imported')
