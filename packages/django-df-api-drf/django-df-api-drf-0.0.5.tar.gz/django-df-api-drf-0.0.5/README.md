# Django DF API DRF

Module for automatic including Djangoflow apps API to your project.

## Installation:

- Install the package

```
pip install django-df-api-drf
```

- Add the package to your INSTALLED_APPS

```
INSTALLED_APPS = [
    ...
    'df_api_drf',
    ...
]
```

- Add the package to your urls.py

```
urlpatterns = [
    ...
    path("api/v1/", include("df_api_drf.urls")),
    ...
]
```
