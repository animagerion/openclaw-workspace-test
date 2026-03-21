#!/usr/bin/env python3
"""
Script to insert an image into a Google Doc.
Uses OAuth with the gogcli credentials.
"""

import os
import sys
import json
import argparse
import socket
import threading
import webbrowser
from urllib.parse import urlparse, parse_qsl

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file',
]

TOKEN_DIR = os.path.expanduser('~/.config/gogcli')
TOKEN_FILE = os.path.join(TOKEN_DIR, 'docs_token.json')
CLIENT_SECRET_FILE = os.path.join(TOKEN_DIR, 'client_secret.json')


def find_free_port():
    """Find a free port."""
    with socket.socket() as s:
        s.bind(('', 0))
        return s.getsockname()[1]


def run_manual_flow(flow):
    """Run OAuth flow manually (for headless environments)."""
    port = find_free_port()
    flow.redirect_uri = f'http://localhost:{port}'
    
    auth_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    
    print(f"\n{'='*60}")
    print("AUTORIZACION GOOGLE OAUTH")
    print(f"{'='*60}")
    print(f"\n1. Abre esta URL en tu navegador:\n")
    print(f"   {auth_url}\n")
    print(f"2. Autoriza con tu cuenta de Google (animagerion@gmail.com)")
    print(f"3. Seras redirigido a una URL tipo: http://localhost:{port}/?code=...&state=...")
    print(f"4. COPIA esa URL completa de la barra de direcciones y pegala aqui\n")
    print(f"{'='*60}\n")
    
    # Wait for the redirect
    redirect_url = input("Pega la URL de redireccion aqui: ").strip()
    
    # Exchange code for tokens
    flow.fetch_token(authorization_response=redirect_url)
    return flow.credentials


def load_or_refresh_token():
    """Load existing token or do OAuth flow."""
    creds = None
    
    # Try to load existing token
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            creds = Credentials.from_authorized_user_info(json.load(f), SCOPES)
    
    # If no valid token, do OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refrescando token...")
            creds.refresh(Request())
        else:
            print("Haciendo OAuth flow...")
            if os.path.exists(CLIENT_SECRET_FILE):
                flow = InstalledAppFlow.from_client_secrets_file(
                    CLIENT_SECRET_FILE, SCOPES)
                creds = run_manual_flow(flow)
            else:
                print(f"Client secret file not found at {CLIENT_SECRET_FILE}")
                sys.exit(1)
        
        # Save token for next time
        with open(TOKEN_FILE, 'w') as f:
            f.write(creds.to_json())
    
    return creds


def get_drive_service(creds):
    """Build Drive API service."""
    return build('drive', 'v3', credentials=creds, cache_discovery=False)


def get_docs_service(creds):
    """Build Docs API service."""
    return build('docs', 'v1', credentials=creds, cache_discovery=False)


def upload_image_to_drive(drive_service, image_path, filename=None):
    """Upload image to Drive and get the file ID."""
    if filename is None:
        filename = os.path.basename(image_path)
    
    file_metadata = {
        'name': filename,
        'mimeType': 'image/png',
    }
    
    media = MediaFileUpload(image_path, mimetype='image/png', resumable=True)
    
    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, name, webViewLink, webContentLink'
    ).execute()
    
    # Make the file publicly readable
    try:
        drive_service.permissions().create(
            fileId=file['id'],
            body={'type': 'anyone', 'role': 'reader'}
        ).execute()
    except:
        pass
    
    return file


def insert_image_from_drive(docs_service, drive_service, doc_id, image_path, filename=None, width=650):
    """Upload image to Drive and insert it into the doc."""
    print(f"Subiendo imagen a Drive...")
    drive_file = upload_image_to_drive(drive_service, image_path, filename)
    print(f"Subido: {drive_file['name']} (ID: {drive_file['id']})")
    print(f"URL: {drive_file.get('webViewLink', 'N/A')}")
    
    # Get document end index
    doc = docs_service.documents().get(documentId=doc_id).execute()
    end_index = doc.get('body', {}).get('content', [{}])[-1].get('endIndex', 1)
    
    # Calculate proportional height (assuming original is ~800 wide)
    height_magnitude = (width / 800) * 500
    
    requests = [
        {'insertText': {'location': {'index': end_index - 1}, 'text': '\n\n'}},
        {
            'insertInlineImage': {
                'location': {'index': end_index - 1},
                'uri': drive_file.get('webContentLink') or drive_file.get('webViewLink'),
                'objectSize': {
                    'width': {'magnitude': width, 'unit': 'PT'},
                    'height': {'magnitude': height_magnitude, 'unit': 'PT'},
                }
            }
        },
        {'insertText': {'location': {'index': end_index - 1}, 'text': f'\n{drive_file["name"]}\n'}},
    ]
    
    result = docs_service.documents().batchUpdate(
        documentId=doc_id,
        body={'requests': requests}
    ).execute()
    
    print(f"Imagen insertada en el documento")
    return result


def main():
    parser = argparse.ArgumentParser(description='Insert image into Google Doc')
    parser.add_argument('doc_id', help='Google Doc ID')
    parser.add_argument('image_path', help='Path to image file')
    parser.add_argument('--width', type=int, default=650, help='Image width in points (default: 650)')
    parser.add_argument('--name', help='Filename in Drive (default: original filename)')
    
    args = parser.parse_args()
    
    print("Cargando credenciales...")
    creds = load_or_refresh_token()
    
    drive_service = get_drive_service(creds)
    docs_service = get_docs_service(creds)
    
    insert_image_from_drive(docs_service, drive_service, args.doc_id, args.image_path, args.name, args.width)
    print("Hecho!")


if __name__ == '__main__':
    main()
