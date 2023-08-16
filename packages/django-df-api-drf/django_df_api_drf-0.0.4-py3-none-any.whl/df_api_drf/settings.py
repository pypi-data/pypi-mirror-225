from typing import Any, Dict

from django.conf import settings
from rest_framework.settings import APISettings

DEFAULTS: Dict[str, Any] = {}

module_settings = APISettings(
    getattr(settings, "DJANGOFLOW", {}).get("DF_API_DRF"), DEFAULTS
)
