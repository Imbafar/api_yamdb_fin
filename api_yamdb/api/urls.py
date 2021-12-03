from .views import CategoriesViewSet, GenresViewSet, TitlesViewSet
from .views import UsersViewSet, signup_new_user, get_token
from django.urls import include, path
from rest_framework import routers

router_v1 = routers.DefaultRouter()

router_v1.register('categories', CategoriesViewSet)
router_v1.register('genres', GenresViewSet)
router_v1.register('titles', TitlesViewSet)
router_v1.register('users', UsersViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', signup_new_user, name='auth_signup'),
    path('v1/auth/token/', get_token, name='auth_token')
]
