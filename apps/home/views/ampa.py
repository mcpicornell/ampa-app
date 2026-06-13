import logging
from zoneinfo import ZoneInfo

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import login_required
from django.shortcuts import redirect, render

from apps.home.ampa import (
    AmpaFileControllerDependencies,
    get_ampa_file_controller,
    get_ampa_images_storage,
    get_ampa_reader_agent,
    get_ampa_result_calculator,
    get_gemini_policy,
    get_home_blood_pressure_filter,
    get_local_json_service,
)
from apps.home.ampa.constants import AI_FREE_QUOTA_EXCEEDED_MESSAGE

logger = logging.getLogger(__name__)

controller = get_ampa_file_controller(
    AmpaFileControllerDependencies(
        storage_service=get_ampa_images_storage(),
        local_json_service=get_local_json_service(settings.LOCAL_JSON_DIR),
        filter_service=get_home_blood_pressure_filter(),
        calculator=get_ampa_result_calculator(),
        ampa_reader_agent=get_ampa_reader_agent(
            models=settings.GEMINI_MODELS,
            api_key=settings.GEMINI_API_KEY,
            llm_policy=get_gemini_policy(ZoneInfo("America/Los_Angeles")),
        ),
    )
)


@login_required(login_url="/login/")
def ampa_upload(request):
    if request.method == "POST" and request.FILES.get("ampa_file"):
        try:
            file = request.FILES["ampa_file"]
            registry_id = controller.save_ampa_file(file)
            return redirect("ampa_result", registry_id=registry_id)

        except Exception as e:
            error_message = f"Error uploading AMPA file: {e}"
            logger.error(error_message)

            if AI_FREE_QUOTA_EXCEEDED_MESSAGE in error_message:
                error_message = "AI free quota exceeded, try it again tomorrow"

            messages.error(request, error_message)
            return render(request, "home/ampa-file-upload.html")

    return render(request, "home/ampa-file-upload.html")


@login_required(login_url="/login/")
def ampa_result(request, registry_id):
    try:
        result = controller.calculate_ampa_result(registry_id)
        return render(
            request,
            "home/ampa-result.html",
            {"result": result, "registry_id": registry_id},
        )
    except Exception as e:
        error_message = f"Error calculating AMPA result: {e}"
        logger.error(error_message)
        messages.error(request, error_message)
        return render(request, "home/ampa-file-upload.html")
