from .views import CategoriesViewSet, GenresViewSet, TitlesViewSet
from django.urls import include, path
from rest_framework import routers

router_v1 = routers.DefaultRouter()

router_v1.register('categories', CategoriesViewSet)
router_v1.register('genres', GenresViewSet)
router_v1.register('titles', TitlesViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
