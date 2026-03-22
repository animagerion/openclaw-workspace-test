#!/usr/bin/env python3
"""
Autenticación Google Calendar mediante Device Flow (para CLI)
"""
from google_auth_oauthlib.flow import InstalledAppFlow

client_config = {
    'installed': {
        'client_id': 'REDACTED_CLIENT_ID',
        'client_secret': 'REDACTED_CLIENT_SECRET',
        'redirect_uris': ['http://localhost'],
        'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
        'token_uri': 'https://oauth2.googleapis.com/token'
    }
}

SCOPES = ['https://www.googleapis.com/auth/calendar']

flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
creds = flow.run_console()

print(f"Access token: {creds.token[:30]}...")
print(f"Refresh token: {creds.refresh_token}")
