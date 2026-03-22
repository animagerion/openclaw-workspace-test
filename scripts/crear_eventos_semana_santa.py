#!/usr/bin/env python3
"""
Crear eventos de Semana Santa Utrera 2026 en Google Calendar
"""
import json
import os
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    """Autenticarse con Google Calendar usando gogcli token"""
    creds_data = json.load(open(os.path.expanduser('~/.config/gogcli/keyring/token:animagerion@gmail.com')))
    
    creds = Credentials.from_authorized_user_info(
        info={
            "token": creds_data.get('token', ''),
            "refresh_token": creds_data.get('refresh_token', ''),
            "token_uri": "https://oauth2.googleapis.com/token",
            "client_id": creds_data.get('client_id', ''),
            "client_secret": creds_data.get('client_secret', ''),
            "scopes": SCOPES
        }
    )
    
    service = build('calendar', 'V3', credentials=creds)
    return service

def parse_time(time_str):
    """Convertir string de hora a datetime"""
    return datetime.strptime(time_str, "%H:%M").time()

def create_event(service, summary, date, start_time, end_time, description="", location="Utrera"):
    """Crear un evento en Google Calendar"""
    start_dt = datetime.combine(date, start_time)
    
    # Si la hora de fin es menor que la de inicio, significa que es al día siguiente
    if end_time < start_time:
        end_dt = datetime.combine(date + timedelta(days=1), end_time)
    else:
        end_dt = datetime.combine(date, end_time)
    
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_dt.isoformat(),
            'timeZone': 'Europe/Madrid',
        },
        'end': {
            'dateTime': end_dt.isoformat(),
            'timeZone': 'Europe/Madrid',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 30},
            ],
        },
    }
    
    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"  ✅ Evento creado: {summary} ({start_dt.strftime('%d/%m %H:%M')})")
    return event

def main():
    print("Conectando con Google Calendar...")
    service = get_calendar_service()
    
    # Leer datos JSON
    with open('/home/gerion/.openclaw/workspace/semana_santa_utrera_2026.json', 'r') as f:
        data = json.load(f)
    
    print(f"\nCreando eventos para {data['nombre']}...\n")
    
    # Crear un calendario específico para Semana Santa
    calendar_body = {
        'summary': 'Semana Santa Utrera 2026',
        'description': 'Programa de procesiones y actos de Semana Santa en Utrera 2026',
        'timeZone': 'Europe/Madrid'
    }
    
    try:
        calendar = service.calendars().insert(body=calendar_body).execute()
        calendar_id = calendar['id']
        print(f"✅ Calendario creado: {calendar['summary']}\n")
    except Exception as e:
        print(f"Usando calendario primario (calendario ya podría existir)\n")
        calendar_id = 'primary'
    
    eventos_creados = 0
    
    for procesion in data['procesiones']:
        hermandad = procesion['hermandad']
        fecha = datetime.strptime(procesion['fecha'], '%Y-%m-%d')
        nombre_completo = procesion.get('nombre_completo', hermandad)
        sede = procesion.get('sede', 'Utrera')
        itinerary = procesion.get('itinerario', [])
        
        # 1. Evento de SALIDA
        if procesion.get('hora_salida'):
            hora_salida = parse_time(procesion['hora_salida'])
            desc = f"Hermandad: {nombre_completo}\nSede: {sede}"
            if itinerary:
                desc += f"\n\nItinerario:\n" + "\n".join([f"• {p}" for p in itinerary])
            
            create_event(
                service, 
                f"🕯️ SALIDA: {hermandad}",
                fecha.date(),
                hora_salida,
                (datetime.combine(fecha.date(), hora_salida) + timedelta(minutes=30)).time(),
                description=desc,
                location=sede
            )
            eventos_creados += 1
        
        # 2. Evento de CARRERA OFICIAL (si está en el itinerario)
        for idx, punto in enumerate(itinerario):
            if 'Carrera Oficial' in punto:
                # Extraer hora de la cadena "Carrera Oficial (HH:MM h)"
                hora_str = punto.split('(')[1].split(' ')[0] if '(' in punto else None
                if hora_str:
                    hora_co = datetime.strptime(hora_str, '%H:%M').time()
                    create_event(
                        service,
                        f"📍 {hermandad} - Carrera Oficial",
                        fecha.date(),
                        hora_co,
                        (datetime.combine(fecha.date(), hora_co) + timedelta(minutes=15)).time(),
                        description=f"{hermandad} pasa por la Carrera Oficial",
                        location="Carrera Oficial, Utrera"
                    )
                    eventos_creados += 1
        
        # 3. Evento de RECOGIDA
        if procesion.get('hora_recogida'):
            hora_recogida = parse_time(procesion['hora_recogida'])
            create_event(
                service,
                f"🏠 RECOGIDA: {hermandad}",
                fecha.date(),
                hora_recogida,
                (datetime.combine(fecha.date(), hora_recogida) + timedelta(minutes=30)).time(),
                description=f"La Hermandad {hermandad} regresa a su sede",
                location=sede
            )
            eventos_creados += 1
    
    print(f"\n🎉 Total: {eventos_creados} eventos creados")

if __name__ == '__main__':
    main()
