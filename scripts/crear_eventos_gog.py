#!/usr/bin/env python3
"""
Crear eventos de Semana Santa Utrera 2026 en Google Calendar usando gog CLI
"""
import json
import subprocess
import os
from datetime import datetime, timedelta

GOG_BIN = "/home/gerion/.linuxbrew/Homebrew/Cellar/gogcli/0.9.0/bin/gog"
ACCOUNT = "animagerion@gmail.com"
CALENDAR_ID = "animagerion@gmail.com"

def run_gog(args):
    """Ejecutar comando gog con el password del keyring"""
    env = os.environ.copy()
    env["GOG_KEYRING_PASSWORD"] = "gerion-gog-2026"
    cmd = [GOG_BIN] + args + ["--account", ACCOUNT]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, env=env, check=False)
        if result.returncode != 0:
            print(f"  ⚠️ Error: {result.stderr.strip() if result.stderr else 'Unknown'}")
            return None
        return result.stdout
    except Exception as e:
        print(f"  ⚠️ Exception: {e}")
        return None

def parse_time(time_str):
    """Convertir string de hora a datetime.time"""
    return datetime.strptime(time_str, "%H:%M").time()

def format_datetime(date_obj, time_obj, days_offset=0):
    """Formatear como RFC3339"""
    dt = datetime.combine(date_obj, time_obj) + timedelta(days=days_offset)
    return dt.strftime('%Y-%m-%dT%H:%M:00+02:00')

def main():
    # Leer datos JSON
    with open('/home/gerion/.openclaw/workspace/semana_santa_utrera_2026.json', 'r') as f:
        data = json.load(f)
    
    print(f"Creando eventos para {data['nombre']}...\n")
    
    eventos_creados = 0
    
    for procesion in data['procesiones']:
        hermandad = procesion['hermandad']
        fecha = datetime.strptime(procesion['fecha'], '%Y-%m-%d').date()
        nombre_completo = procesion.get('nombre_completo', hermandad)
        sede = procesion.get('sede') or 'Utrera'
        itinerario = procesion.get('itinerario', [])
        
        desc_base = f"Hermandad: {nombre_completo}\\nSede: {sede}"
        if itinerario:
            desc_base += f"\\n\\nItinerario:\\n" + "\\n".join([f"• {p}" for p in itinerario])
        
        # 1. SALIDA
        if procesion.get('hora_salida'):
            hora_salida = parse_time(procesion['hora_salida'])
            hora_fin_dt = (datetime.combine(fecha, hora_salida) + timedelta(minutes=30))
            
            print(f"Creando: 🕯️ SALIDA: {hermandad}")
            run_gog([
                "calendar", "create", CALENDAR_ID,
                "--summary", f"🕯️ SALIDA: {hermandad}",
                "--from", format_datetime(fecha, hora_salida),
                "--to", hora_fin_dt.strftime('%Y-%m-%dT%H:%M:00+02:00'),
                "--description", desc_base,
                "--location", sede,
                "--reminder", "popup:30m"
            ])
            eventos_creados += 1
        
        # 2. CARRERA OFICIAL
        for idx, punto in enumerate(itinerario):
            if 'Carrera Oficial' in punto:
                try:
                    hora_str = punto.split('(')[1].split(' ')[0]
                    hora_co = datetime.strptime(hora_str, '%H:%M').time()
                    hora_fin_dt = (datetime.combine(fecha, hora_co) + timedelta(minutes=15))
                    
                    print(f"Creando: 📍 {hermandad} - Carrera Oficial")
                    run_gog([
                        "calendar", "create", CALENDAR_ID,
                        "--summary", f"📍 {hermandad} - Carrera Oficial",
                        "--from", format_datetime(fecha, hora_co),
                        "--to", hora_fin_dt.strftime('%Y-%m-%dT%H:%M:00+02:00'),
                        "--description", f"{hermandad} pasa por la Carrera Oficial",
                        "--location", "Carrera Oficial, Utrera"
                    ])
                    eventos_creados += 1
                except:
                    pass
        
        # 3. RECOGIDA
        if procesion.get('hora_recogida'):
            hora_recogida = parse_time(procesion['hora_recogida'])
            # La recogida puede ser al día siguiente si es medianoche
            days_offset = 1 if hora_recogida.hour < 6 else 0
            hora_fin_dt = (datetime.combine(fecha, hora_recogida) + timedelta(days=days_offset, minutes=30))
            
            print(f"Creando: 🏠 RECOGIDA: {hermandad}")
            run_gog([
                "calendar", "create", CALENDAR_ID,
                "--summary", f"🏠 RECOGIDA: {hermandad}",
                "--from", format_datetime(fecha, hora_recogida, days_offset),
                "--to", hora_fin_dt.strftime('%Y-%m-%dT%H:%M:00+02:00'),
                "--description", f"La Hermandad {hermandad} regresa a su sede",
                "--location", sede
            ])
            eventos_creados += 1
    
    print(f"\n🎉 Total: {eventos_creados} eventos creados en {CALENDAR_ID}")

if __name__ == '__main__':
    main()
