from .views import CategoriesViewSet, GenresViewSet, TitlesViewSet
from .views import AllUsersViewSet, UserViewSet, signup_new_user, get_token
from django.urls import include, path
from rest_framework import routers

router_v1 = routers.DefaultRouter()

router_v1.register('categories', CategoriesViewSet)
router_v1.register('genres', GenresViewSet)
router_v1.register('titles', TitlesViewSet)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', signup_new_user, name='auth_signup'),
    path('v1/auth/token/', get_token, name='auth_token'),
    path(
        'v1/users/',
        AllUsersViewSet.as_view(
            {'get': 'list', 'post': 'create'}
        ),
        name='all_users'
    ),
    path(
        'v1/users/<slug:username>/',
        UserViewSet.as_view(
            {'get': 'retrieve', 'patch': 'partial_update', 'del': 'destroy'}
        ),
        name='user'
    ),
]
