import os
from dotenv import load_dotenv
from api.api_key_generation import APIKeyGeneratorService

load_dotenv()

admin_email = os.getenv("ADMIN_EMAIL")
admin_api_key = os.getenv("ADMIN_API_KEY")


def generateAPIKey(email: str):
    api_service = APIKeyGeneratorService(admin_email, admin_api_key)
    api_key = api_service.generate_api_key("vendor2@example.com")
    print(api_key)
    return api_key
