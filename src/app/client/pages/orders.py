import streamlit as st
import pandas as pd
from api.orders import OrdersService
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()
vendor_email = os.getenv("VENDOR_EMAIL")
vendor_api_key = os.getenv("VENDOR_API_KEY")

print(vendor_api_key, vendor_email)

# Initialize SessionStore and AuthService
orders_service = OrdersService(vendor_email, vendor_api_key)


json_response = orders_service.get_orders()

orders = pd.json_normalize(json_response['orders'])
orders.index = range(1, len(orders) + 1)

# Create a Streamlit app for the Order Page
st.title('Orders')
col1, col2, col3 = st.columns(3)
col1.metric("Total Orders", len(orders), "Order Dashboard")
col2.metric("Total Order Value", "Rs 12345", "Order Dashboard")

# Define a function to open the modal for adding an order


def create_order_modal():
    with st.form(key='create_order_form'):
        st.header('Place a New Order')

        # Add input fields for order information
        product_name = st.text_input('Product Name')
        quantity = st.number_input('Quantity', min_value=1)
        customer_name = st.text_input('Customer Name')
        order_description = st.text_area('Order Description')

        # Add a submit button
        submit_button = st.form_submit_button('Place Order')

        if submit_button:
            # You can process the order data here and add it to your data source
            # For example, you can add it to a DataFrame or send it to a database

            # Assuming you have a data source called 'orders_data' as a list of dictionaries
            new_order = {
                'Product Name': product_name,
                'Quantity': quantity,
                'Customer Name': customer_name,
                'Order Description': order_description,
                'Order ID': len(orders_data) + 1
            }
            orders_data.append(new_order)

            # Clear the form fields
            st.text_input('Product Name', value='')
            st.number_input('Quantity', min_value=1)
            st.text_input('Customer Name', value='')
            st.text_area('Order Description', value='')


# Check if the 'Place Order' button is clicked
if st.button('Place Order'):
    create_order_modal()

# Display the order information table
st.title('Order Information Table')

# Define the order data as a list of dictionaries
orders_data = [
    {
        'Product Name': 'Product A',
        'Quantity': 2,
        'Customer Name': 'Customer A',
        'Order Description': 'Description A',
        'Order ID': 1
    },
    {
        'Product Name': 'Product B',
        'Quantity': 3,
        'Customer Name': 'Customer B',
        'Order Description': 'Description B',
        'Order ID': 2
    },
    {
        'Product Name': 'Product C',
        'Quantity': 1,
        'Customer Name': 'Customer C',
        'Order Description': 'Description C',
        'Order ID': 3
    }
]

# Create a DataFrame from the order data
# df = pd.DataFrame(orders_data)

# Display the table using st.dataframe
st.dataframe(orders, width=1000, height=len(orders))
