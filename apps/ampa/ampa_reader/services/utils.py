import base64
from typing import BinaryIO


def encode_image(file: BinaryIO) -> str:
    return base64.b64encode(file.read()).decode("utf-8")
