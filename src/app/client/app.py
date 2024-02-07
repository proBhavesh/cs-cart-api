import streamlit as st
from kinde_sdk import Configuration
from kinde_sdk.kinde_api_client import KindeApiClient, GrantType
from authlib.common.security import generate_token
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

KINDE_HOST = os.getenv("KINDE_HOST")
KINDE_CLIENT_ID = os.getenv("KINDE_CLIENT_ID")
KINDE_CLIENT_SECRET = os.getenv("KINDE_CLIENT_SECRET")
KINDE_REDIRECT_URL = os.getenv("KINDE_REDIRECT_URL")
KINDE_POST_LOGOUT_REDIRECT_URL = os.getenv("KINDE_POST_LOGOUT_REDIRECT_URL")

# Kinde Configuration
configuration = Configuration(host=KINDE_HOST)
CODE_VERIFIER = generate_token(48)
kinde_api_client_params = {
    "configuration": configuration,
    "domain": KINDE_HOST,
    "client_id": KINDE_CLIENT_ID,
    "client_secret": KINDE_CLIENT_SECRET,
    "grant_type": GrantType.AUTHORIZATION_CODE,
    "callback_url": KINDE_REDIRECT_URL,
    "code_verifier": CODE_VERIFIER,
}

kinde_client = KindeApiClient(**kinde_api_client_params)

# a = kinde_client.get_login_url()

a = kinde_client.is_authenticated()

print(a)


# http://localhost:8501/?code=olKeN-9JyTJpV8OD25WONmwI5HhwUp5_Rb3BY8XrzYs.sqwX_Z_dhCYaNA8HabzcrFgb0JvMHyFRdXBCCqvztbU&scope=openid%20profile%20email%20offline&state=wauk1eXEQ7q242u2nwo0Z2XgWi8hqm
# Streamlit UI
# st.title('Streamlit App with Kinde Authentication')

# if 'access_token' not in st.session_state:
#     st.session_state['access_token'] = None

# if st.session_state['access_token'] is None:
#     login_url = kinde_client.get_login_url()
#     st.sidebar.markdown(f"[Login with Kinde]({login_url})")
# else:
#     user_details = kinde_client.get_user_details()
#     print("this is user details",user_details)
#     user_email = user_details.get('email', 'No email available')
#     st.sidebar.write(f"Welcome {user_details['given_name']} {user_details['family_name']}")
#     st.sidebar.write(f"Email: {user_email}")

#     if st.sidebar.button('Logout'):
#         logout_url = kinde_client.logout(redirect_to=KINDE_POST_LOGOUT_REDIRECT_URL)
#         st.session_state['access_token'] = None
#         st.experimental_rerun()
