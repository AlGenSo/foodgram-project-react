from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('users', views.UserViewSet, basename='users')
router.register('recipes', views.RecipesViewSet, basename='recipes')
router.register('ingredients', views.IngredientViewSet, basename='ingredients')
router.register('tags', views.TagViewSet, basename='tags')
router.register(
    r'users/(?P<users_id>\d+)/subscribe',
    views.UserViewSet,
    basename='subscribe'
)
router.register(
    r'users/subscriptions/',
    views.UserViewSet,
    basename='subscriptions'
)
router.register(
    r'recipes/(?P<recipes_id>\d+)/favorite',
    views.RecipesViewSet,
    basename='favorite'
)
router.register(
    r'recipes/(?P<recipes_id>\d+)/shopping_cart',
    views.RecipesViewSet,
    basename='shopping_cart'
)
router.register(
    r'recipes/download_shopping_cart',
    views.RecipesViewSet,
    basename='download_shopping_cart'
)


urlpatterns = [
    path('', include(router.urls)),
    path(r'auth/', include('djoser.urls')),
    path(r'auth/', include('djoser.urls.authtoken')),
]
