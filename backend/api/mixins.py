from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets


class RetrieveMixinViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """Mixin для Ingredient и Tag"""
    pagination_class = None
    filter_backends = [DjangoFilterBackend, ]
    search_fields = ('name',)
