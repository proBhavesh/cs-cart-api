from base64 import b64encode

# This module is the initialization for the API package of the cs-cart API wrapper.
# It sets up basic configurations and utilities needed by the API modules.

# BASE_URL is the root URL for all CS-Cart API requests. This should be set to the
# URL of the CS-Cart store that the API will interact with.
BASE_URL = "https://shop.migoiq.app"


def encode_credentials(email: str, api_key: str) -> str:
    """
    Encodes the provided email and API key into a Base64 encoded string.

    This function is a utility to generate the necessary authentication header
    value for making API requests to the CS-Cart store. The CS-Cart API uses
    Basic HTTP authentication, which requires a Base64 encoded string of the
    format 'email:api_key'.

    Args:
        email (str): The email of the user accessing the CS-Cart API.
        api_key (str): The API key associated with the user's account.

    Returns:
        str: A Base64 encoded string in the format 'email:api_key', suitable
             for use in an HTTP 'Authorization' header for Basic auth.
    """
    return b64encode(f"{email}:{api_key}".encode()).decode()
