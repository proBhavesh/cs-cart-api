import streamlit as st
import pandas as pd
from api.shipments import ShipmentService
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()
vendor_email = os.getenv("VENDOR_EMAIL")
vendor_api_key = os.getenv("VENDOR_API_KEY")

# Initialize SessionStore and AuthService
product_service = ShipmentService(vendor_email, vendor_api_key)

# Use AuthService to send authentication requests
json_response = product_service.send_auth_request()

shipment = pd.DataFrame()

if 'shipment' in json_response:
    shipment = pd.json_normalize(json_response['shipment'])
    shipment.index = range(1, len(shipment) + 1)
else:
    st.write("'shipment' data not found in the API response")


# Create a Streamlit app for the Shipment Page
st.title('Shipments')
col1, col2, col3 = st.columns(3)
col1.metric("Total Shipments", len(shipment), "Shipment Dashboard")
col2.metric("Total Shipment Value", "Rs 0", "Shipment Dashboard")

# Define a function to open the modal for adding a shipment


def create_shipment_modal():
    with st.form(key='create_shipment_form'):
        st.header('Add a New Shipment')

        # Add input fields for shipment information
        shipment_name = st.text_input('Shipment Name')
        shipment_value = st.text_input('Shipment Value')
        shipment_destination = st.text_input('Destination')
        shipment_description = st.text_area('Shipment Description')

        # Add a submit button
        submit_button = st.form_submit_button('Add Shipment')

        if submit_button:
            # You can process the shipment data here and add it to your data source
            # For example, you can add it to a DataFrame or send it to a database

            # Assuming you have a data source called 'shipments_data' as a list of dictionaries
            new_shipment = {
                'Shipment Name': shipment_name,
                'Shipment Value': shipment_value,
                'Destination': shipment_destination,
                'Shipment Description': shipment_description,
                'Shipment ID': len(shipments_data) + 1
            }
            shipments_data.append(new_shipment)

            # Clear the form fields
            st.text_input('Shipment Name', value='')
            st.text_input('Shipment Value', value='')
            st.text_input('Destination', value='')
            st.text_area('Shipment Description', value='')


# Check if the 'Add Shipment' button is clicked
if st.button('Add Shipment'):
    create_shipment_modal()

# Display the shipment information table
st.title('Shipment Information Table')

# Define the shipment data as a list of dictionaries
shipments_data = [
    {
        'Shipment Name': 'Shipment A',
        'Shipment Value': 'Rs 1000',
        'Destination': 'Location A',
        'Shipment Description': 'Description A',
        'Shipment ID': 1
    },
    {
        'Shipment Name': 'Shipment B',
        'Shipment Value': 'Rs 2000',
        'Destination': 'Location B',
        'Shipment Description': 'Description B',
        'Shipment ID': 2
    },
    {
        'Shipment Name': 'Shipment C',
        'Shipment Value': 'Rs 1500',
        'Destination': 'Location C',
        'Shipment Description': 'Description C',
        'Shipment ID': 3
    }
]


# Display the table using st.dataframe
st.dataframe(shipment, width=1000, height=len(shipment))
