import streamlit as st
from streamlit_oauth import OAuth2Component
import os
import base64
import json
from dotenv import load_dotenv
from streamlit_cookies_controller import CookieController


from utils.helpers import generateAPIKey

load_dotenv()
controller = CookieController()

# create an OAuth2Component instance
CLIENT_ID = os.getenv("KINDE_CLIENT_ID")
CLIENT_SECRET = os.getenv("KINDE_CLIENT_SECRET")
KINDE_DOMAIN = os.getenv("KINDE_DOMAIN")
AUTHORIZE_ENDPOINT = f"https://{KINDE_DOMAIN}/oauth2/auth"
TOKEN_ENDPOINT = f"https://{KINDE_DOMAIN}/oauth2/token"
REVOKE_ENDPOINT = f"https://{KINDE_DOMAIN}/oauth2/revoke"
KINDE_REDIRECT_URI = os.getenv("KINDE_REDIRECT_URI")

if controller.get("email"):
    st.write("You are already logged in!")
    controller.set("email", controller.get("email"))
    controller.set("token", controller.get("token"))
    st.write(controller.get("email"))
    if st.button("Logout"):
        controller.remove("email")
        controller.remove("token")
        st.experimental_rerun()
else:
    st.title("KINDE OIDC Example")
    st.write(
        "This example shows how to use the raw OAuth2 component to authenticate with a Kinde OAuth2."
    )
    oauth2 = OAuth2Component(
        CLIENT_ID,
        CLIENT_SECRET,
        AUTHORIZE_ENDPOINT,
        TOKEN_ENDPOINT,
        TOKEN_ENDPOINT,
        REVOKE_ENDPOINT,
    )
    result = oauth2.authorize_button(
        name="Continue with Kinde",
        icon="https://kinde.com/icon.svg",
        redirect_uri=KINDE_REDIRECT_URI,
        scope="openid email profile",
        key="kinde",
        use_container_width=True,
    )
    st.write(result)

    if result:
        # Decode the ID token to get the user's email address
        st.write("This is inside result")
        id_token = result["token"]["id_token"]
        payload = id_token.split(".")[1]
        payload += "=" * (-len(payload) % 4)  # Correct padding for Base64 decoding
        email = json.loads(base64.b64decode(payload)).get("email")
        # Set session state and cookies
        controller.set("email", email)
        controller.set("token", result["token"])

        st.rerun()
