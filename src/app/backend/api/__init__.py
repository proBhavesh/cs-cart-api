from base64 import b64encode


BASE_URL = "https://shop.migoiq.app"


def encode_credentials(email: str, api_key: str) -> str:
    """return Base64 encoded string"""
    return b64encode(f"{email}:{api_key}".encode()).decode()
