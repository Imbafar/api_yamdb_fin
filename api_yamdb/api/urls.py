from .views import CategoriesViewSet, GenresViewSet, TitlesViewSet
from .views import AllUsersViewSet, UserViewSet
from django.urls import include, path
from rest_framework import routers
# from rest_framework_simplejwt.views import TokenObtainPairView

router_v1 = routers.DefaultRouter()

router_v1.register('categories', CategoriesViewSet)
router_v1.register('genres', GenresViewSet)
router_v1.register('titles', TitlesViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    # path('v1/auth/signup/', include(router_v1.urls)),
    # path(
    #     'v1/auth/token/',
    #     TokenObtainPairView.as_view(),
    #     name='token_obtain_pair'
    # ),
    path(
        'v1/users/',
        AllUsersViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='users_all'
    ),
    path(
        'v1/users/<slug:username>/',
        UserViewSet.as_view(
            {'get': 'retrieve', 'patch': 'partial_update', 'del': 'destroy'}
        ),
        name='user'
    ),
]
