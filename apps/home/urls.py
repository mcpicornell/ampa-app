# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from django.views.generic import RedirectView

from apps.home import views

urlpatterns = [
    path("upload-ampa/", views.ampa_upload, name="ampa_upload"),
    path("ampa-result/<str:result_id>/", views.ampa_result, name="ampa_result"),
    # The home page
    path("", RedirectView.as_view(pattern_name="ampa_upload", permanent=False)),
    path("", views.index, name="home"),
    # Matches any html file
    re_path(r"^.*\.*", views.pages, name="pages"),
]
