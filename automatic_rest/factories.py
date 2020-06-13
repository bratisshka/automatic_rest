from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from automatic_rest.filters import FieldsFilterBackend


def build_serializer(model, model_alias):
    serializer_meta = type('Meta', (), {'model': model, 'fields': '__all__'})
    serializer_class = type(
        f"{model_alias}Serializer",
        (ModelSerializer,),
        {
            'Meta': serializer_meta
        })
    return serializer_class


def build_viewset(model, model_alias):
    viewset_class = type(
        f"{model_alias}ViewSet",
        (ModelViewSet,),
        {
            'filter_backends': [filters.OrderingFilter, FieldsFilterBackend],
            'pagination_class': LimitOffsetPagination}
    )
    viewset_class.queryset = model.objects.order_by('pk')
    viewset_class.serializer_class = build_serializer(model, model_alias)
    return viewset_class
