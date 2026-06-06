import asyncio
import datetime
from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand

from apps.home.ampa.controller import get_ampa_file_controller
from apps.home.ampa.entities import HomeBloodPressureRegistry


class Command(BaseCommand):
    def handle(self, *args, **options):
        asyncio.run(self.async_handle(*args, **options))

    async def async_handle(self, *args, **options):
        file_path = Path(__file__).resolve().parent / "ampa.jpeg"

        with open(file_path, "rb") as f:
            file = SimpleUploadedFile(
                name="ampa.jpeg",
                content=f.read(),
                content_type="image/jpeg",
            )
        controller = get_ampa_file_controller(json_debug_active=True)
        datetime_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        registry: HomeBloodPressureRegistry = await controller.upload_ampa_file(
            file, datetime_str
        )
        result = await controller.calculate_ampa_result(registry, datetime_str)
        print("Done")
