import base64


def encode_image(file):
    return base64.b64encode(file.read()).decode("utf-8")
