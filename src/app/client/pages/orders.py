from ast import arg
from math import prod
from xxlimited import new
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
orders = pd.json_normalize(json_response["orders"])
orders.index = range(1, len(orders) + 1)

# Create a Streamlit app for the Order Page
st.title("Orders")
col1, col2, col3 = st.columns(3)
col1.metric("Total Orders", len(orders), "Order Dashboard")
col2.metric("Total Order Value", "Rs 12345", "Order Dashboard")


def submitted():
    new_order = {
        "Product Name": st.session_state["Product Name"],
        "Quantity": st.session_state["Quantity"],
        "Customer Name": st.session_state["Customer Name"],
        "Order Description": st.session_state["Order Description"],
        "Order ID": len(orders) + 1,
    }

    response = orders_service.create_order(new_order)
    if response:
        st.success(response)
    else:
        st.error("Failed to place order. Please try again.")

    # reset()


# def reset():
#     st.session_state.submitted = False
#     st.session_state["Product Name"] = ""
#     st.session_state["Quantity"] = 1
#     st.session_state["Customer Name"] = ""
#     st.session_state["Order Description"] = ""


with st.form(key="create_order_form"):
    st.header("Place a New Order")

    st.text_input("Product Name", key="Product Name")
    st.number_input("Quantity", min_value=1, key="Quantity")
    st.text_input("Customer Name", key="Customer Name")
    st.text_area("Order Description", key="Order Description")

    submit_button = st.form_submit_button("Place Order")

if submit_button:
    submitted()

# Display the order information table
st.title("Order Information Table")
st.dataframe(orders, width=1000, height=len(orders) * 24)
