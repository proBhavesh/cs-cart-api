# Import the necessary libraries
import streamlit as st
import jwt
import requests
from urllib.parse import urlencode
from streamlit_option_menu import option_menu
from descope import (
    REFRESH_SESSION_TOKEN_NAME,
    SESSION_TOKEN_NAME,
    AuthException,
    DeliveryMethod,
    DescopeClient,
)

# Navbar
# with st.sidebar:
#     selected = option_menu(
#         menu_title="Main Menu",
#         options=["Home", "Product", "About", "Contact"],
#         icons=["house-door", "bi-box-seam", "bi-person", "bi-envelope"],
#         menu_icon="cast",
#         default_index=0,
#     )

# if selected == "Home":
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
# Define constants for project ID and flow ID
PROJECT_ID = "P2S34yZ72qTTPfxD45n4Er0Qlws3"
FLOW_ID = "sign-up-or-in"

# Create Descope client
try:
    descope_client = DescopeClient(project_id=PROJECT_ID)
except Exception as error:
    print("Failed to initialize Descope client. Error:")
    print(error)

    # Store session token if exists
session_token = st.session_state.get("token", None)

# Define helper function to check JWT token validity


def is_jwt_expired(token):
    decoded_token = jwt.decode(token, options={"verify_signature": False})
    return decoded_token["exp"] < time.time()

    # Check session token and JWT expiration
not_valid_token = session_token and is_jwt_expired(session_token)

# Show Descope login if no token or token is expired
if not session_token or not_valid_token:
    # Descope login URL
    descope_url = "http://localhost:8501"

    tenant_email = "vendor@example.com"
    # Create a button that when clicked will redirect user to Descope login
    if st.button("Log In With Descope Flows"):
        try:
            resp = descope_client.saml.start(
                tenant=tenant_email, return_url=descope_url)
            print("Successfully started saml auth. URL: ")
            print(resp)
        except AuthException as error:
            print("Failed to start saml auth")
            print("Status Code: " + str(error.status_code))
            print("Error: " + str(error.error_message))

            # Redirect to Descope login
        st.write(
            f'<a href="{descope_url}" target="_blank">Go to Descope Login</a>',
            unsafe_allow_html=True,
        )

    # If logged in (i.e., valid token exists), display user info
if session_token and not not_valid_token:
    try:
        # Validate the session token with Descope
        jwt_response = descope_client.validate_session(
            session_token=session_token)

        # If successful, display user info
        st.write(f"Successfully validated user session:")
        st.write(jwt_response)
    except Exception as error:
        st.write("Could not validate user session. Error:")
        st.write(error)

# elif selected == "About":
#     st.write("This is the About page.")
# elif selected == "Product":
#     st.write("This is the Product page.")

# elif selected == "Contact":
#     st.write("This is the Contact page.")
