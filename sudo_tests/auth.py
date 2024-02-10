import os
from dotenv import load_dotenv
from api.api_key_generation import APIKeyGeneratorService

# Load environment variables
load_dotenv()
admin_email = os.getenv("ADMIN_EMAIL")
admin_api_key = os.getenv("ADMIN_API_KEY")

print(admin_email, admin_api_key)

# Initialize AuthService
api_service = APIKeyGeneratorService(admin_email, admin_api_key)
api_key = api_service.generate_api_key("bhaveshjat9950@gmail.com")
print(api_key)
