import streamlit as st
from streamlit_oauth import OAuth2Component
import os
import base64
import json
import extra_streamlit_components as stx
from dotenv import load_dotenv

from utils.helpers import generateAPIKey

load_dotenv()

cookie_manager = stx.CookieManager(key="outer_cookie")
if cookie_manager.get(cookie="email"):
    email = cookie_manager.get(cookie="email")
    st.write(email)


# create an OAuth2Component instance
CLIENT_ID = os.getenv("KINDE_CLIENT_ID")
CLIENT_SECRET = os.getenv("KINDE_CLIENT_SECRET")
KINDE_DOMAIN = os.getenv("KINDE_DOMAIN")
AUTHORIZE_ENDPOINT = f"https://{KINDE_DOMAIN}/oauth2/auth"
TOKEN_ENDPOINT = f"https://{KINDE_DOMAIN}/oauth2/token"
REVOKE_ENDPOINT = f"https://{KINDE_DOMAIN}/oauth2/revoke"
KINDE_REDIRECT_URI = os.getenv("KINDE_REDIRECT_URI")

if "auth" not in st.session_state:
    # cookie_manager = stx.CookieManager()
    st.title("KINDE OIDC Example")
    st.write(
        "This example shows how to use the raw OAuth2 component to authenticate with a Kinde OAuth2 ."
    )

    # create a button to start the OAuth2 flow
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

    if result:
        st.write(result)
        # decode the id_token jwt and get the user's email address
        id_token = result["token"]["id_token"]
        # verify the signature is an optional step for security
        payload = id_token.split(".")[1]
        # add padding to the payload if needed
        payload += "=" * (-len(payload) % 4)
        payload = json.loads(base64.b64decode(payload))
        # print(payload)
        email = payload["email"]
        st.session_state["auth"] = email
        st.session_state["token"] = result["token"]
        st.rerun()
else:
    cookie_manager = stx.CookieManager(key="inner_cookie")
    st.write("You are logged in!")
    st.write(st.session_state["auth"])
    st.write(st.session_state["token"])
    # print(st.session_state["token"])
    # print(generateAPIKey(st.session_state["auth"]))
    cookie_manager.set("email", st.session_state["auth"], key="email")
    cookie_manager.set("token", st.session_state["token"], key="token_auth")
    if st.button("Logout"):
        del st.session_state["auth"]
        del st.session_state["token"]
