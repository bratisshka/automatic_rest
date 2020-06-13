from rest_framework import filters
from rest_framework.settings import api_settings

EXCLUDE_FIELDS = {
    api_settings.ORDERING_PARAM,
    'limit',
    'offset'
}


class FieldsFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        query_params = set(request.query_params.keys())
        existing_fields = {field.name for field in queryset.model._meta.fields}
        filter_fields = {
            key: request.query_params[key]
            for key in query_params.intersection(existing_fields).difference(EXCLUDE_FIELDS)
        }
        try:
            return queryset.filter(**filter_fields)
        except ValueError:
            return queryset.none()
