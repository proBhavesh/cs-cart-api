import streamlit as st
import pandas as pd
import requests
from api.stores import StoresService
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()
vendor_email = os.getenv("VENDOR_EMAIL")
vendor_api_key = os.getenv("VENDOR_API_KEY")

print(vendor_api_key, vendor_email)

# Initialize Session and StoresService
store_service = StoresService(vendor_email, vendor_api_key)

# Fetch all stores
json_response = store_service.get_stores()

stores = pd.json_normalize(json_response['stores'])
stores.index = range(1, len(stores) + 1)

st.title('Stores')

col1, col2, col3 = st.columns(3)
col1.metric("Total stores", len(stores), "Store Dashboard")
col2.metric("Total Sales", "Rs 2345", "Sales Dashboard")
# col3.metric("Humidity", "86%", "4%")


if st.button('Create Store'):
    # Create a modal for creating a new store
    with st.form(key='create_store_form'):
        st.header('Create a New Store')

        # Add input fields for store name and description
        store_name = st.text_input('Store Name')
        store_email = st.text_input('Store Email')
        store_description = st.text_area('Store Description')

        # Add a submit button
        submit_button = st.form_submit_button('Create Store')

    if submit_button:
        # Define the store data
        store_data = {
            "company": store_name,
            "storefront": store_email,
            "secure_storefront": store_description,
            "clone_from": "2",
            "clone": {
                "layouts": "i",
                "settings": "Yi",
                "products": "Yi",
                "categories": "iY"
            }
        }

        # Define the API endpoint for creating a store
        # Replace with the actual URL
        create_store_url = "http://localhost:8501/test/test_stores"

        # Send a POST request to create the store
        response = requests.post(create_store_url, json=store_data)

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            json_response = response.json()  # Parse the JSON response
            st.success(f'Store created successfully. Store Name: {store_name}')
        else:
            st.error(
                'Failed to create the store. Please check the server response.')


# data = {
#     'SL Number': [1, 2, 3, 4, 5],
#     'Store Name': ['Store A', 'Store B', 'Store C', 'Store D', 'Store E'],
#     'Created Date': ['2023-10-01', '2023-10-02', '2023-10-03', '2023-10-04', '2023-10-05'],
#     'Store Description': ['Description A', 'Description B', 'Description C', 'Description D', 'Description E']
# }


# Create a Streamlit app
st.title('Store Information Table')

# Add Edit and Delete buttons with icons
# edit_icon = "https://image.flaticon.com/icons/svg/565/565026.svg"
# delete_icon = "https://image.flaticon.com/icons/svg/3221/3221897.svg"

stores['Actions'] = [f"[Edit]| [Delete]" for _ in range(len(stores))]

# Display the table using st.dataframe
st.dataframe(stores, width=800, height=len(stores))
