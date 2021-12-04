from .views import CategoriesViewSet, GenresViewSet, TitlesViewSet
from .views import UsersViewSet, signup_new_user, get_token
from django.urls import include, path
from rest_framework import routers

from .views import (CategoriesViewSet, CommentsViewSet, GenresViewSet,
                    ReviewViewSet, TitlesViewSet)

app_name = 'api'

router_v1 = routers.DefaultRouter()

router_v1.register('categories', CategoriesViewSet)
router_v1.register('genres', GenresViewSet)
router_v1.register('titles', TitlesViewSet)
router_v1.register('users', UsersViewSet)
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review')
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', signup_new_user, name='auth_signup'),
    path('v1/auth/token/', get_token, name='auth_token')
]
