import datetime
import logging
import uuid

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import login_required
from django.shortcuts import redirect, render
from pydantic import BaseModel

from apps.home.ampa.constants import AI_FREE_QUOTA_EXCEEDED_MESSAGE
from apps.home.ampa.controller import get_ampa_file_controller
from apps.home.ampa.entities import HomeBloodPressureRegistry

logger = logging.getLogger(__name__)

ONE_DAY = 60 * 60 * 24


class RegistrySession(BaseModel):
    datetime: str
    registry: HomeBloodPressureRegistry


@login_required(login_url="/login/")
def ampa_upload(request):
    if request.method == "POST" and request.FILES.get("ampa_file"):
        try:
            file = request.FILES["ampa_file"]
            controller = get_ampa_file_controller(settings.JSON_DEBUG_ACTIVE)
            datetime_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            registry: HomeBloodPressureRegistry = controller.upload_ampa_file(
                file, datetime_str
            )

            result_id = str(uuid.uuid4())
            request.session.setdefault("ampa_registries", {})
            request.session["ampa_registries"][result_id] = RegistrySession(
                datetime=datetime_str,
                registry=registry,
            ).model_dump()
            request.session.modified = True
            request.session.set_expiry(ONE_DAY)
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

    registries = request.session.get("ampa_registries", {})
    session_dict = registries.get(result_id)

    if not session_dict:
        messages.error(request, f"Registry '{result_id}' not found")
        return render(request, "home/ampa-file-upload.html")

    controller = get_ampa_file_controller(settings.JSON_DEBUG_ACTIVE)
    session = RegistrySession(**session_dict)
    result = controller.calculate_ampa_result(session.registry, session.datetime)

    return render(
        request, "home/ampa-result.html", {"result": result, "result_id": result_id}
    )
