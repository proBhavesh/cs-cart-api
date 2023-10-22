from api.auth import AuthService
from api.store import SessionStore
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
admin_email = os.getenv("ADMIN_EMAIL")
admin_api_key = os.getenv("ADMIN_API_KEY")

# Initialize SessionStore and AuthService
session_store = SessionStore()
auth_service = AuthService(session_store, admin_email, admin_api_key)

# Use AuthService to send authentication requests
print(auth_service.send_auth_request("vendor@example.com"))
# print(auth_service.send_auth_request("vendor2@example.com"))

# # Import GetPagesService class from GetPagesService.py
# from getpages import GetPagesService

# # Initialize GetPagesService with admin email and API key
# get_pages_service = GetPagesService(
#     "vendor@example.com", "1T5W3C21870R410Y47c814Rck3l2v215"
# )

# # Define parameters for the GET request
# params = {
#     "page": 1,
#     "items_per_page": 10,
#     "sort_by": "position",
#     "sort_order": "desc",
# }

# # Send request to get pages with parameters
# response = get_pages_service.send_pages_request(params)

# # Print the response
# print(response)


# List language variables
lang_code = "en"  # substitute with the required language code
print(auth_service.get_langvars(lang_code))

# Get specific language variable
name = "test_variable"  # substitute with the required variable name
print(auth_service.get_langvar(name, lang_code))

# Create a new language variable
new_name = "new_test_var"
new_value = "This is a new test variable."
print(auth_service.create_langvar(new_name, new_value, lang_code))

# Update a language variable
updated_value = "This is an updated value for the variable."
print(auth_service.update_langvar(name, updated_value, lang_code))

# Delete a language variable
delete_name = "to_be_deleted_var"  # substitute with the variable to be deleted
print(auth_service.delete_langvar(delete_name))


# List installed languages
print(auth_service.get_languages())

# Get specific language
lang_id = 1  # Substitute with required language ID
print(auth_service.get_language(lang_id))

# Create a new language
lang_code = "ts"
name = "New Language"
status = "A"
country_code = "US"
print(auth_service.create_language(lang_code, name, status, country_code))

# Update a language
updated_name = "Updated Language"
updated_status = "H"
updated_country_code = "RU"
print(auth_service.update_language(lang_id, lang_code,
      updated_name, updated_status, updated_country_code))

# Delete a language
delete_lang_id = 3  # Substitute with the ID of the language to be deleted
print(auth_service.delete_language(delete_lang_id))
