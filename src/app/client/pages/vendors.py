import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from api.vendors import VendorsService

# Load environment variables
load_dotenv()
vendor_email = os.getenv("VENDOR_EMAIL")
vendor_api_key = os.getenv("VENDOR_API_KEY")

# Initialize VendorsService
vendor_service = VendorsService(vendor_email, vendor_api_key)

# Fetch vendor data
json_response = vendor_service.get_vendors()

print(json_response)
# Initialize an empty DataFrame for vendors
vendors_data = pd.DataFrame()

if "vendors" in json_response:
    # Normalize JSON data and create DataFrame
    vendors_data = pd.json_normalize(json_response["vendors"])
    vendors_data.index = range(1, len(vendors_data) + 1)
else:
    st.write("No vendor data available in the API response.")

# Streamlit app layout
st.title("Vendor Management")
col1, col2, col3 = st.columns(3)
col1.metric("Total Vendors", len(vendors_data), "Vendor Dashboard")


# Function to create a modal for adding a vendor
def create_vendor_modal():
    with st.form(key="create_vendor_form"):
        st.header("Add a New Vendor")

        vendor_name = st.text_input("Vendor Name")
        vendor_contact = st.text_input("Contact Information")
        vendor_address = st.text_input("Address")
        vendor_description = st.text_area("Vendor Description")

        submit_button = st.form_submit_button("Add Vendor")

        if submit_button:
            new_vendor = {
                "company": vendor_name,
                "email": vendor_contact,
                "address": vendor_address,
                "description": vendor_description,
            }
            # Add new vendor to vendors_data DataFrame
            global vendors_data
            vendors_data = vendors_data.append(new_vendor, ignore_index=True)

            # Reset the form fields
            st.text_input("Vendor Name", value="", key="1")
            st.text_input("Contact Information", value="", key="2")
            st.text_input("Address", value="", key="3")
            st.text_area("Vendor Description", value="", key="4")


# Button to add a new vendor
if st.button("Add Vendor"):
    create_vendor_modal()

# Display the vendor information table
st.title("Vendor Information Table")
st.dataframe(vendors_data, width=1000, height=len(vendors_data) * 200)
