import os.path

import google_auth_oauthlib.flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# OAuth 2.0 Client ID downloaded from https://console.cloud.google.com/apis/credentials
UNAUTHORIZED_CREDENTIALS = "client_secret.json"

# Will be created once any user authorizes access to their account by running this script
AUTHORIZED_CREDENTIALS = 'token.json'

def get_youtube_credentials():
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    credentials = None
    if os.path.exists(AUTHORIZED_CREDENTIALS):
        credentials = Credentials.from_authorized_user_file(AUTHORIZED_CREDENTIALS, scopes)
        if credentials:
            if credentials.valid:
                return credentials
            if credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
                return credentials
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        UNAUTHORIZED_CREDENTIALS, scopes)
    credentials = flow.run_console()
    with open(AUTHORIZED_CREDENTIALS, 'w') as token:
        token.write(credentials.to_json())
    return credentials
