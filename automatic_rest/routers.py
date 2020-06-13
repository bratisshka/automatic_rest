import django.apps as apps
from rest_framework.routers import DefaultRouter

from automatic_rest.factories import build_viewset


class AutomaticApiRouter(DefaultRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        model_list = apps.apps.get_models()
        for model in model_list:
            model_alias = f"{model._meta.app_label}_{model.__name__.lower()}"
            viewset_class = build_viewset(model, model_alias)
            self.register(model_alias, viewset_class, basename=model_alias)
