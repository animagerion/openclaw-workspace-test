#!/usr/bin/env python3
"""
Script para obtener token de Google Calendar mediante OAuth
"""
import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/calendar']

client_config = {
    'installed': {
        'client_id': 'REDACTED_CLIENT_ID',
        'client_secret': 'REDACTED_CLIENT_SECRET',
        'redirect_uris': ['http://localhost'],
        'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
        'token_uri': 'https://oauth2.googleapis.com/token'
    }
}

def main():
    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    creds = flow.run_local_server(port=8888, prompt='consent', access_type='offline')
    
    # Guardar token
    token_data = {
        'token': creds.token,
        'refresh_token': creds.refresh_token,
        'token_uri': creds.token_uri,
        'client_id': creds.client_id,
        'client_secret': creds.client_secret,
        'scopes': creds.scopes
    }
    
    token_path = os.path.expanduser('~/.config/gogcli/keyring/token:calendar_utrera')
    with open(token_path, 'w') as f:
        json.dump(token_data, f)
    
    print(f"✅ Token guardado en: {token_path}")
    print(f"Refresh token: {creds.refresh_token[:20]}...")

if __name__ == '__main__':
    main()
