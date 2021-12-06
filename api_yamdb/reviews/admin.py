from django.contrib import admin

from .models import Categories, Comments, Custom_User, Genres, Review, Title

admin.site.register(Categories)
admin.site.register(Genres)
admin.site.register(Title)
admin.site.register(Custom_User)
admin.site.register(Review)
admin.site.register(Comments)
