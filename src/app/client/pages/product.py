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

product_service = ProductsService(vendor_email, vendor_api_key)

json_response = product_service.get_products()

products = pd.json_normalize(json_response['products'])
products.index = range(1, len(products) + 1)

# Create a Streamlit app
st.title('Products')
col1, col2, col3 = st.columns(3)
col1.metric("Total Products",  len(products), "Products Dashboard")
col2.metric("Total Sales", "Rs 2345", "Sales Dashboard")
# Define a function to open the modal for adding a product


def create_product_modal():
    with st.form(key='create_product_form'):
        st.header('Add a New Product')

        # Add input fields for product information
        product_name = st.text_input('Product Name')
        product_cost = st.text_input('Product Cost')
        product_image = st.file_uploader(
            'Product Image', type=['jpg', 'png', 'jpeg'])
        product_description = st.text_area('Product Description')

        # Add a submit button
        submit_button = st.form_submit_button('Add Product')

        if submit_button:
            # You can process the product data here and add it to your data source
            # For example, you can add it to a DataFrame or send it to a database

            # Assuming you have a data source called 'products_data' as a list of dictionaries
            new_product = {
                'Product Name': product_name,
                'Product Cost': product_cost,
                'Product Image': product_image,
                'Product Description': product_description,
                'Product ID': len(products_data) + 1
            }
            products_data.append(new_product)

            # Clear the form fields
            st.text_input('Product Name', value='')
            st.text_input('Product Cost', value='')
            st.file_uploader('Product Image', type=['jpg', 'png', 'jpeg'])
            st.text_area('Product Description', value='')


# Check if the 'Add Product' button is clicked
if st.button('Add Product'):
    create_product_modal()

# Display the product information table
st.title('Product Information Table')

# Define the product data as a list of dictionaries
# products_data = [
#     {
#         'Product Name': 'Product A',
#         'Product Cost': 'Rs 100',
#         'Product Image': None,
#         'Product Description': 'Description A',
#         'Product ID': 1
#     },
#     {
#         'Product Name': 'Product B',
#         'Product Cost': 'Rs 200',
#         'Product Image': None,
#         'Product Description': 'Description B',
#         'Product ID': 2
#     },
#     {
#         'Product Name': 'Product C',
#         'Product Cost': 'Rs 150',
#         'Product Image': None,
#         'Product Description': 'Description C',
#         'Product ID': 3
#     }
# ]

# Create a DataFrame from the product data
# df = pd.DataFrame(products_data)

# Display the table using st.dataframe
# st.dataframe(df, width=1000, height=600)


# Convert your JSON response to a DataFrame
products = pd.json_normalize(json_response['products'])
# print(json_response)

# Display table using st.dataframe
st.dataframe(products, width=1200, height=len(products)*2)
