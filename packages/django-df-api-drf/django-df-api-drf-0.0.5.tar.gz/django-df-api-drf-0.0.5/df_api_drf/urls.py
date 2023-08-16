from collections import defaultdict
from typing import Dict

from django.apps import apps
from django.conf.urls import include
from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

app_name = "df_api_drf"

urlpatterns = []

namespaces: Dict[str, Dict[str, str]] = defaultdict(dict)

for app in apps.get_app_configs():
    if hasattr(app, "api_path"):
        for namespace, urls in getattr(
            app, "api_drf_namespaces", {"v1": f"{app.name}.drf.urls"}
        ).items():
            namespaces[namespace][app.api_path] = urls


for namespace, app_urls in namespaces.items():
    namespace_patterns = []
    for api_path, urls in app_urls.items():
        namespace_patterns += [path(api_path, include((urls, api_path.strip("/"))))]
    urlpatterns += [path(f"{namespace}/", include((namespace_patterns, namespace)))]


urlpatterns += [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("", SpectacularRedocView.as_view(url_name="df_api_drf:schema"), name="redoc"),
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="df_api_drf:schema"),
        name="swagger-ui",
    ),
]
