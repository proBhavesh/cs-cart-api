import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from api.products import ProductsService

# Load environment variables
load_dotenv()
vendor_email = os.getenv("VENDOR_EMAIL")
vendor_api_key = os.getenv("VENDOR_API_KEY")

# Initialize ProductsService
product_service = ProductsService(vendor_email, vendor_api_key)

# Streamlit app for Products Page
st.title("Products")


# Function to handle product creation
def submitted_product():
    new_product = {
        "product": st.session_state["Product Name"],
        # "Category ID": st.session_state["Category ID"],
        "price": st.session_state["Price"],
    }

    response = product_service.create_product(new_product)
    if response:
        st.success(response)
    else:
        st.error("Failed to add product. Please try again.")


# Create a form for adding a new product
with st.form(key="create_product_form"):
    st.header("Add a New Product")

    st.text_input("Product Name", key="Product Name")
    # st.text_input("Category ID", key="Category ID")
    st.text_input("Price", key="Price")

    submit_button = st.form_submit_button("Add Product")

if submit_button:
    submitted_product()

# Fetch products from the API
json_response = product_service.get_products()
products = pd.json_normalize(json_response["products"])
products.index = range(1, len(products) + 1)

# Display metrics and product information table
col1, col2, col3 = st.columns(3)
col2.metric("Total Products", len(products))
st.title("Product Information Table")
st.dataframe(products, width=1000, height=len(products) * 24)
