import datetime
import logging
from zoneinfo import ZoneInfo

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import login_required
from django.shortcuts import redirect, render

from apps.home.ampa.constants import AI_FREE_QUOTA_EXCEEDED_MESSAGE
from apps.home.ampa.controller import get_ampa_file_controller
from apps.home.ampa.entities import HomeBloodPressureRegistry
from apps.home.ampa.services import get_gemini_policy
from apps.home.registries_storage import (
    CreateRegistryItem,
    GetRegistryItem,
    RegistryItem,
    get_registries_storage,
)

logger = logging.getLogger(__name__)

controller = get_ampa_file_controller(
    models=settings.GEMINI_MODELS,
    llm_api_key=settings.GEMINI_API_KEY,
    json_dir=settings.LOCAL_JSON_DIR,
    json_debug_active=settings.JSON_DEBUG_ACTIVE,
    llm_policy=get_gemini_policy(ZoneInfo("America/Los_Angeles")),
)
registries_storage = get_registries_storage()


@login_required(login_url="/login/")
def ampa_upload(request):
    if request.method == "POST" and request.FILES.get("ampa_file"):
        try:
            file = request.FILES["ampa_file"]
            datetime_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            registry: HomeBloodPressureRegistry = controller.upload_ampa_file(
                file, datetime_str
            )

            registry_item: RegistryItem = registries_storage.save_registry(
                CreateRegistryItem(datetime_str, registry)
            )
            return redirect("ampa_result", result_id=registry_item.result_id)

        except Exception as e:
            error_message = str(e)
            logger.error(f"Error uploading AMPA file: {error_message}")

            if AI_FREE_QUOTA_EXCEEDED_MESSAGE in error_message:
                error_message = "AI free quota exceeded, try it again tomorrow"

            messages.error(request, error_message)
            return render(request, "home/ampa-file-upload.html")

    return render(request, "home/ampa-file-upload.html")


@login_required(login_url="/login/")
def ampa_result(request, result_id):
    registry_item: RegistryItem | None = registries_storage.get_registry(
        GetRegistryItem(result_id)
    )

    if registry_item is None:
        messages.error(request, f"Registry '{result_id}' not found or expired")
        return render(request, "home/ampa-file-upload.html")

    result = controller.calculate_ampa_result(
        registry_item.registry, registry_item.datetime
    )

    return render(
        request, "home/ampa-result.html", {"result": result, "result_id": result_id}
    )
