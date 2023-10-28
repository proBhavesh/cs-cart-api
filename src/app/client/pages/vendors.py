import streamlit as st
import pandas as pd

# Create a Streamlit app for the Vendor Page
st.title('Vendor Management')
col1, col2, col3 = st.columns(3)
col1.metric("Total Vendors", "50", "Vendor Dashboard")

# Define a function to open the modal for adding a vendor
def create_vendor_modal():
    with st.form(key='create_vendor_form'):
        st.header('Add a New Vendor')

        # Add input fields for vendor information
        vendor_name = st.text_input('Vendor Name')
        vendor_contact = st.text_input('Contact Information')
        vendor_address = st.text_input('Address')
        vendor_description = st.text_area('Vendor Description')

        # Add a submit button
        submit_button = st.form_submit_button('Add Vendor')

        if submit_button:
            # You can process the vendor data here and add it to your data source
            # For example, you can add it to a DataFrame or send it to a database

            # Assuming you have a data source called 'vendors_data' as a list of dictionaries
            new_vendor = {
                'Vendor Name': vendor_name,
                'Contact Information': vendor_contact,
                'Address': vendor_address,
                'Vendor Description': vendor_description,
                'Vendor ID': len(vendors_data) + 1
            }
            vendors_data.append(new_vendor)

            # Clear the form fields
            st.text_input('Vendor Name', value='')
            st.text_input('Contact Information', value='')
            st.text_input('Address', value='')
            st.text_area('Vendor Description', value='')

# Check if the 'Add Vendor' button is clicked
if st.button('Add Vendor'):
    create_vendor_modal()

# Display the vendor information table
st.title('Vendor Information Table')

# Define the vendor data as a list of dictionaries
vendors_data = [
    {
        'Vendor Name': 'Vendor A',
        'Contact Information': 'vendora@example.com',
        'Address': '123 Main St, City, Country',
        'Vendor Description': 'Description A',
        'Vendor ID': 1
    },
    {
        'Vendor Name': 'Vendor B',
        'Contact Information': 'vendorb@example.com',
        'Address': '456 Elm St, City, Country',
        'Vendor Description': 'Description B',
        'Vendor ID': 2
    },
    {
        'Vendor Name': 'Vendor C',
        'Contact Information': 'vendorc@example.com',
        'Address': '789 Oak St, City, Country',
        'Vendor Description': 'Description C',
        'Vendor ID': 3
    }
]

# Create a DataFrame from the vendor data
df = pd.DataFrame(vendors_data)

# Display the table using st.dataframe
st.dataframe(df, width=1000, height=len(df) * 200)
