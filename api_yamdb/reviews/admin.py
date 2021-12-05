from django.contrib import admin

from .models import (Categories, Genres, Titles,
                     Review, Comments, Custom_User)

admin.site.register(Categories)
admin.site.register(Genres)
admin.site.register(Titles)
admin.site.register(Custom_User)
admin.site.register(Review)
admin.site.register(Comments)
