from django.urls import include, path

from automatic_rest.routers import AutomaticApiRouter

automatic_router = AutomaticApiRouter()
urlpatterns = [
    path("api/", include(automatic_router.urls)),
]
