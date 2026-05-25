import base64

from django.core.files.uploadedfile import UploadedFile


def encode_image(file: UploadedFile) -> str:
    return base64.b64encode(file.read()).decode("utf-8")
