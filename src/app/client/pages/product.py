import streamlit as st
import pandas as pd
from api.products import ProductsService
import os
from dotenv import load_dotenv
import json

load_dotenv()
vendor_email = os.getenv("VENDOR_EMAIL")
vendor_api_key = os.getenv("VENDOR_API_KEY")
print(vendor_api_key, vendor_email)
# product_service = ProductsService(vendor_email, vendor_api_key)


# Create a Streamlit app
st.title('Products')

# Define a function to open the modal for adding a product


def create_product_modal():
    print("Entered create_product_modal function")
    with st.form(key='create_product_form'):
        print("Inside st.form")
        submit_button = st.form_submit_button('Add Product')

        if submit_button:
            print("Form submitted")
    print('Exited create_product_modal function')


# json_response = product_service.get_products()
# Convert your JSON response to a DataFrame
# products = pd.json_normalize(json_response['products'])
# products.index = range(1, len(products) + 1)
# print(json_response)


col1, col2, col3 = st.columns(3)
# col1.metric("Total Products",  len(products), "Products Dashboard")
col2.metric("Total Sales", "Rs 2345", "Sales Dashboard")


# Check if the 'Add Product' button is clicked
if st.button('Add Product'):
    print("Add Product button clicked")
    create_product_modal()
    print("create_product_modal function call has finished")

# Display the product information table
st.title('Product Information Table')


# Display table using st.dataframe
# st.dataframe(products, width=1200, height=len(products)*2)
