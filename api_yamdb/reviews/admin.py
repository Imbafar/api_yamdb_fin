from django.contrib import admin

from .models import (Categories, Genres, Title,
                     Review, Comments, Custom_User)

admin.site.register(Categories)
admin.site.register(Genres)
admin.site.register(Title)
admin.site.register(Custom_User)
admin.site.register(Review)
admin.site.register(Comments)
