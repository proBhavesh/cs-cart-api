# Import the necessary libraries
import streamlit as st
import jwt
import requests
from urllib.parse import urlencode
from descope import (
    REFRESH_SESSION_TOKEN_NAME,
    SESSION_TOKEN_NAME,
    AuthException,
    DeliveryMethod,
    DescopeClient,
)

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
    descope_url = "https://auth.descope.io/{PROJECT_ID}?flow={FLOW_ID}"

    # Create a button that when clicked will redirect user to Descope login
    if st.button("Log In With Descope Flows"):
       
        
        # Redirect to Descope login
        st.write(
            f'<a href="{descope_url}" target="_blank">Go to Descope Login</a>',
            unsafe_allow_html=True,
        )

# If logged in (i.e., valid token exists), display user info
elif session_token and not not_valid_token:
    try:
        # Validate the session token with Descope
        jwt_response = descope_client.validate_session(session_token=session_token)

        # If successful, display user info
        st.write(f"Successfully validated user session:")
        st.write(jwt_response)
    except Exception as error:
        st.write("Could not validate user session. Error:")
        st.write(error)
