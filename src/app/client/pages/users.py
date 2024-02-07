import streamlit as st
import pandas as pd
from api.users import UserService
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()
vendor_email = os.getenv("VENDOR_EMAIL")
vendor_api_key = os.getenv("VENDOR_API_KEY")

print(vendor_api_key, vendor_email)

# Initialize Session and StoresService
user_service = UserService(vendor_email, vendor_api_key)


# Fetch all users
json_response = user_service.get_users()
users = pd.json_normalize(json_response["users"])
users.index = range(1, len(users) + 1)

# Create a Streamlit app for the User Page
st.title("User Management")
col1, col2, col3 = st.columns(3)
col1.metric("Total Users", "123", "User Dashboard")

# Define a function to open the modal for adding a user


def create_user_modal():
    with st.form(key="create_user_form"):
        st.header("Add a New User")

        # Add input fields for user information
        user_name = st.text_input("User Name")
        user_email = st.text_input("Email")
        user_role = st.selectbox("Role", ["Admin", "User"])
        user_description = st.text_area("User Description")

        # Add a submit button
        submit_button = st.form_submit_button("Add User")

        if submit_button:
            # You can process the user data here and add it to your data source
            # For example, you can add it to a DataFrame or send it to a database

            # Assuming you have a data source called 'users_data' as a list of dictionaries
            new_user = {
                "User Name": user_name,
                "Email": user_email,
                "Role": user_role,
                "User Description": user_description,
                "User ID": len(users_data) + 1,
            }
            users_data.append(new_user)

            # Clear the form fields
            st.text_input("User Name", value="")
            st.text_input("Email", value="")
            st.selectbox("Role", ["Admin", "User"])
            st.text_area("User Description", value="")


# Check if the 'Add User' button is clicked
if st.button("Add User"):
    create_user_modal()

# Display the user information table
st.title("User Information Table")

# Define the user data as a list of dictionaries
users_data = [
    {
        "User Name": "User A",
        "Email": "usera@example.com",
        "Role": "User",
        "User Description": "Description A",
        "User ID": 1,
    },
    {
        "User Name": "User B",
        "Email": "userb@example.com",
        "Role": "Admin",
        "User Description": "Description B",
        "User ID": 2,
    },
    {
        "User Name": "User C",
        "Email": "userc@example.com",
        "Role": "User",
        "User Description": "Description C",
        "User ID": 3,
    },
]


# Display the table using st.dataframe
st.dataframe(users, width=1000, height=len(users_data) * 2)
