import time
import uuid

from django.contrib import messages
from django.contrib.auth.views import login_required
from django.shortcuts import redirect, render

from apps.home.ampa.controller import get_ampa_file_controller

ONE_DAY = 60 * 60 * 24


@login_required(login_url="/login/")
def ampa_upload(request):
    if request.method == "POST" and request.FILES.get("ampa_file"):
        try:
            file = request.FILES["ampa_file"]
            controller = get_ampa_file_controller()
            registry = controller.upload_ampa_file(file)

            result_id = str(uuid.uuid4())
            request.session.setdefault("ampa_registries", {})
            request.session["ampa_registries"][result_id] = registry.model_dump()
            request.session.modified = True
            request.session.set_expiry(ONE_DAY)
            return redirect("ampa_result", result_id=result_id)

        except Exception as e:
            messages.error(request, str(e))
            return render(request, "home/ampa-file-upload.html")

    return render(request, "home/ampa-file-upload.html")


@login_required(login_url="/login/")
def ampa_result(request, result_id):

    registries = request.session.get("ampa_registries", {})
    registry = registries.get(result_id)

    if not registry:
        messages.error(request, f"Registry '{result_id}' not found")
        return render(request, "home/ampa-file-upload.html")

    controller = get_ampa_file_controller()
    result = controller.calculate_ampa_result(registry)

    return render(
        request, "home/ampa-result.html", {"result": result, "result_id": result_id}
    )
