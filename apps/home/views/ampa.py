import datetime
import logging
import uuid
from zoneinfo import ZoneInfo

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import login_required
from django.core.cache import cache
from django.shortcuts import redirect, render
from pydantic import BaseModel

from apps.home.ampa.constants import AI_FREE_QUOTA_EXCEEDED_MESSAGE
from apps.home.ampa.controller import get_ampa_file_controller
from apps.home.ampa.entities import HomeBloodPressureRegistry
from apps.home.ampa.services import get_gemini_policy

logger = logging.getLogger(__name__)


class _RegistrySession(BaseModel):
    datetime: str
    registry: HomeBloodPressureRegistry


controller = get_ampa_file_controller(
    models=settings.GEMINI_MODELS,
    llm_api_key=settings.GEMINI_API_KEY,
    json_dir=settings.LOCAL_JSON_DIR,
    json_debug_active=settings.JSON_DEBUG_ACTIVE,
    llm_policy=get_gemini_policy(ZoneInfo("America/Los_Angeles")),
)


@login_required(login_url="/login/")
def ampa_upload(request):
    if request.method == "POST" and request.FILES.get("ampa_file"):
        try:
            file = request.FILES["ampa_file"]
            datetime_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            registry: HomeBloodPressureRegistry = controller.upload_ampa_file(
                file, datetime_str
            )

            result_id = str(uuid.uuid4())

            cache.set(
                f"ampa:{result_id}",
                {
                    "datetime": datetime_str,
                    "registry": registry.model_dump(),
                },
                timeout=settings.CACHE_EXPIRATION,
            )
            return redirect("ampa_result", result_id=result_id)

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
    session_dict = cache.get(f"ampa:{result_id}")

    if not session_dict:
        messages.error(request, f"Registry '{result_id}' not found or expired")
        return render(request, "home/ampa-file-upload.html")

    session = _RegistrySession(**session_dict)

    result = controller.calculate_ampa_result(session.registry, session.datetime)

    return render(
        request, "home/ampa-result.html", {"result": result, "result_id": result_id}
    )
