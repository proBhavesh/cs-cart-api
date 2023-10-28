# example usage
from api.products import ProductsService
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()
vendor_email = os.getenv("VENDOR_EMAIL")
vendor_api_key = os.getenv("VENDOR_API_KEY")

print(vendor_api_key, vendor_email)

# Initialize SessionStore and AuthService
product_service = ProductsService(vendor_email, vendor_api_key)

# Fetch all products
json_response = product_service.get_products()

# Create a new product
# json_response = product_service.create_product("lenovo laptop", [2], "5000")

# new_product_id = json_response["product_id"]
# Update the newly created product
# update_data = {"product": "Apple MacBook Pro", "price": "2000"}
# json_response = product_service.update_product(new_product_id, update_data)

# Delete the product
# json_response = product_service.delete_product(new_product_id)

# product_update_data = {"product": "Updated Lenovo laptop", "price": "5100"}
# json_response = product_service.update_product(1, product_update_data)

# Working with product features
# json_response = product_service.get_product_features(new_product_id)

updated_feature_data = {"product_features": {"Color": "Silver"}}
# json_response = product_service.update_product_features(
#     new_product_id, updated_feature_data)


# Working with variations
variation_group_id = 1  # Assuming it's a valid existing group ID
# json_response = product_service.get_product_variations(variation_group_id)


# Simply adding to a new group
new_variation_data = {"variation_group_id": variation_group_id}
# json_response = product_service.add_product_to_group(
#     new_product_id, new_variation_data)


# json_response = product_service.detach_product_variation(new_product_id)

# json_response = product_service.set_default_variation(new_product_id)


# json_response = product_service.generate_variations(
    # new_product_id, [{"Size": "Medium"}, {"Size": "Large"}])


# Fetch all variation groups
# json_response = product_service.get_variation_groups()


# Data to create a new variation group
group_data = {
    "product_ids": [286, 287, 288],
    "code": "MY_GROUP_1",
    "features": [
        {
            "feature_id": 549,
            "purpose": "group_catalog_item"
        }
    ]
}
# json_response = product_service.create_variation_group(group_data)

# Fetch the newly created variation group
# json_response = product_service.get_variation_group(
    # new_variation_group_id_or_code)

# Update the newly created variation group
update_data = {"code": "MY_GROUP_NEW"}
# json_response = product_service.update_variation_group(
#     new_variation_group_id_or_code, update_data)

# Delete the variation group
# json_response = product_service.delete_variation_group(
#     new_variation_group_id_or_code)


# Get all options of a product
product_id = '12'  # Replace with the actual Product ID
# json_response = product_service.list_product_options(product_id)

# Get details of a specific option
option_id = 3  # Replace with actual Option ID
# json_response = product_service.get_specific_option(option_id)

# Creating a new option
option_data = {
    "product_id": "12",
    "option_name": "Packaging",
    "option_type": "R",
    "required": "Y",
    "inventory": "N",
    "main_pair": {
        "icon": {
            "image_path": {
                "1": "http://example.com/image1.jpg",
                "2": "http://example.com/image2.jpg"
            }
        }
    },
    "variants": {
        "1": {
            "variant_name": "None"
        },
        "2": {
            "variant_name": "Gift wrap",
            "modifier_type": "A",
            "modifier": "5"
        }
    }
}
# json_response = product_service.create_option(option_data)

# Update an existing option
new_option_data = {
    "option_type": "S",
    "main_pair": {
        "icon": {
            "image_path": {
                "2": "http://example.com/image3.jpg",
                "3": "http://example.com/image4.jpg"
            }
        }
    },
    "variants": {
        "2": {
            "variant_name": "Gift wrap"
        },
        "3": {
            "modifier": "20"
        }
    }
}
# json_response = product_service.update_option(option_id, new_option_data)

# Delete an option
# json_response = product_service.delete_option(option_id)
# json_response = product_service.delete_product(1)


# Working with product option combinations
product_id = '12'  # Replace with the actual Product ID

# Fetch all option combinations of a product
# json_response = product_service.list_option_combinations(product_id)

# Get a specific option combination
combination_hash = '822274303'  # replace with actual combination hash
# json_response = product_service.get_option_combination(combination_hash)

# Create a new option combination
combination_data = {
    "24": "74",
}
# json_response = product_service.create_option_combination(
#     product_id, combination_data, amount="34", position="10")

# The new combination_hash after creation, used for update and deletion
# new_combination_hash = json_response.get("combination_hash")

# Update an existing option combination
update_combination_data = {
    "product_code": "Product 34214",
    "amount": "42",
    "position": "0"
}
# json_response = product_service.update_option_combination(
#     new_combination_hash, **update_combination_data)

# Delete an option combination
# json_response = product_service.delete_option_combination(
#     new_combination_hash, product_id)


# List all exceptions for a particular product
product_id = "<Enter product_id here>"
# json_response = product_service.list_exceptions(product_id)

# Get a specific exception
exception_id = "<Enter exception_id here>"
# json_response = product_service.get_exception(exception_id)

# Create a new exception
combination = "<Enter combination data here>"
# json_response = product_service.create_exception(product_id, combination)

# Update an exception
new_combination = "<Enter new combination data here>"
# json_response = product_service.update_exception(exception_id, new_combination)

# Delete an exception
# json_response = product_service.delete_exception(exception_id, product_id)


print(json.dumps(json_response, indent=4))
# print(auth_service.send_auth_request("vendor2@example.com"))
