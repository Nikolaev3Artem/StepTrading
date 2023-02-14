import requests
import os
from dotenv import load_dotenv, find_dotenv
from oauthlib.oauth2 import WebApplicationClient
from flask import request, redirect, url_for
import json
from flask_login import login_user
from app import load_user
from handlers.Hloginbygoogle import client, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
from models.Users import UserLogin
from models.Users import UserLogin

load_dotenv(find_dotenv())

def callback(dbase):
    GOOGLE_DISCOVERY_URL = os.environ.get("GOOGLE_DISCOVERY_URL",None)

    code = request.args.get("code")
    google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
    token_endpoint,
    authorization_response=request.url,
    redirect_url=request.base_url,
    code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        print("User email not available or not verified by Google.")
    user = dbase.addUser(
        username=users_name, email=users_email,isAdmin=False,hpsw=123,balance=0
    )

    # Doesn't exist? Add it to the database.
    if not dbase.getUserByEmail(str(users_email)):
        dbase.addUser(username=users_name, email=users_email,isAdmin=False, hpsw=123,balance=0)

    # Begin user session by logging the user in
    login_user(UserLogin().fromDB(2,dbase))

    # Send user back to homepage
    return redirect(url_for("home"))