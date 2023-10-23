from api.users import UserService
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()
vendor_email = os.getenv("VENDOR_EMAIL")
vendor_api_key = os.getenv("VENDOR_API_KEY")

print(vendor_api_key, vendor_email)

# Initialize Session and StoresService
user_service = UserService(vendor_email, vendor_api_key)


# Fetch all users
json_response = user_service.get_users()
# json_response = user_service.get_users(1, 20)

# Fetch a specific user
# json_response = user_service.get_user('user_id')

# Create a user
user_data = {
    "email": "example@email.com",
    "user_type": "A",  # Admin user
    "company_id": 1,
    "status": "A",   # Active user
    "firstname": "John",
    "lastname": "Doe",
    "company": "Example Company",
    "company_name": "Example Company",
    "is_root": "N",  # Non root user
    "user_login": "john_doe",
    "password": "mypassword"  # Guessing the API may need potentially an md5 hashed password
}
# json_response = user_service.create_user(user)

# Update a user
update_data = {
    "firstname": "Updated name",
    "lastname": "Updated family",
    "company": "Updated Company",
    "company_name": "Updated Company",
    "password": "updatedPassword"
}
# json_response = user_service.update_user('user_id', update_data)

# Delete a user
# json_response = user_service.delete_user('user_id')


# Fetch all usergroups
# json_response = user_service.get_usergroups()

# Fetch a specific usergroup
# json_response = user_service.get_usergroup('group_id')

# Create a usergroup
group_data = {
    "type": "A",
    "status": "A",
    "usergroup": "group_name",
}
# json_response = user_service.create_usergroup(group_data)

# Update a usergroup
group_update_data = {
    "status": "D",  # Disable usergroup
}
# json_response = user_service.update_usergroup('group_id', group_update_data)

# Delete a usergroup
# json_response = user_service.delete_usergroup('group_id')

# Fetch usergroups of specific user
# json_response = user_service.get_user_usergroups('user_id')

# Update user's status in a usergroup
# json_response = user_service.update_user_usergroup_status('user_id', 'group_id', 'A')

# Delete user from a usergroup
# json_response = user_service.delete_user_from_usergroup('user_id', 'group_id')

print(json.dumps(json_response, indent=4))
