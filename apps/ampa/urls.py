# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from django.views.generic import RedirectView

from .views import ampa_result, ampa_upload

urlpatterns = [
    path("upload-ampa/", ampa_upload, name="ampa_upload"),
    path("ampa-result/<str:registry_id>/", ampa_result, name="ampa_result"),
    # The home page
    path("", RedirectView.as_view(pattern_name="ampa_upload", permanent=False)),
]
