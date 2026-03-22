#!/usr/bin/env python3
"""
Crear eventos de Semana Santa Utrera 2026 en Google Calendar
"""
import json
import subprocess
import os
from datetime import datetime, timedelta

GOG_BIN = "/home/gerion/.linuxbrew/Homebrew/Cellar/gogcli/0.9.0/bin/gog"
ACCOUNT = "animagerion@gmail.com"
CALENDAR_ID = "animagerion@gmail.com"

def run_gog(args):
    env = os.environ.copy()
    env["GOG_KEYRING_PASSWORD"] = "gerion-gog-2026"
    cmd = [GOG_BIN] + args + ["--account", ACCOUNT]
    result = subprocess.run(cmd, capture_output=True, text=True, env=env, check=False)
    if result.returncode != 0:
        print(f"  ⚠️ Error: {result.stderr.strip() if result.stderr else 'Unknown'}")
        return None
    return result.stdout

def parse_hour_to_dt(base_date, hour_str):
    """Convert hour string like '24:30', '30:30', '0:30' to (datetime, days_offset)"""
    if hour_str is None:
        return None, 0
    
    parts = hour_str.split(':')
    h = int(parts[0])
    m = int(parts[1]) if len(parts) > 1 else 0
    
    days_offset = h // 24
    real_h = h % 24
    
    dt = datetime(base_date.year, base_date.month, base_date.day, real_h, m) + timedelta(days=days_offset)
    return dt, days_offset

def format_dt(dt):
    return dt.strftime('%Y-%m-%dT%H:%M:00+02:00')

def main():
    with open('/home/gerion/.openclaw/workspace/semana_santa_utrera_2026.json', 'r') as f:
        data = json.load(f)
    
    print(f"Creando eventos para {data['nombre']}...\n")
    
    eventos_creados = 0
    
    for p in data['procesiones']:
        hermandad = p['hermandad']
        fecha = datetime.strptime(p['fecha'], '%Y-%m-%d').date()
        nombre_completo = p.get('nombre_completo', hermandad)
        sede = p.get('sede') or 'Utrera'
        
        desc = f"{nombre_completo}\n{p.get('notas', '')}"
        
        # SALIDA
        if p.get('hora_salida'):
            dt, _ = parse_hour_to_dt(fecha, p['hora_salida'])
            dt_end = dt + timedelta(minutes=30)
            print(f"Creando: 🕯️ SALIDA: {hermandad} ({dt.strftime('%d/%m %H:%M')})")
            run_gog([
                "calendar", "create", CALENDAR_ID,
                "--summary", f"🕯️ SALIDA: {hermandad}",
                "--from", format_dt(dt),
                "--to", format_dt(dt_end),
                "--description", desc,
                "--location", sede,
                "--reminder", "popup:30m"
            ])
            eventos_creados += 1
        
        # CARRERA OFICIAL
        if p.get('hora_carrera_oficial'):
            dt, _ = parse_hour_to_dt(fecha, p['hora_carrera_oficial'])
            dt_end = dt + timedelta(minutes=15)
            print(f"Creando: 📍 {hermandad} - Carrera Oficial ({dt.strftime('%d/%m %H:%M')})")
            run_gog([
                "calendar", "create", CALENDAR_ID,
                "--summary", f"📍 {hermandad} - Carrera Oficial",
                "--from", format_dt(dt),
                "--to", format_dt(dt_end),
                "--description", f"{hermandad} pasa por la Carrera Oficial",
                "--location", "Carrera Oficial, Utrera"
            ])
            eventos_creados += 1
        
        # AYUNTAMIENTO
        if p.get('hora_ayuntamiento'):
            dt, _ = parse_hour_to_dt(fecha, p['hora_ayuntamiento'])
            dt_end = dt + timedelta(minutes=15)
            print(f"Creando: 🏛️ {hermandad} - Ayuntamiento ({dt.strftime('%d/%m %H:%M')})")
            run_gog([
                "calendar", "create", CALENDAR_ID,
                "--summary", f"🏛️ {hermandad} - Ayuntamiento",
                "--from", format_dt(dt),
                "--to", format_dt(dt_end),
                "--description", f"{hermandad} pasa por el Ayuntamiento",
                "--location", "Ayuntamiento, Utrera"
            ])
            eventos_creados += 1
        
        # RECOGIDA
        if p.get('hora_recogida'):
            dt, _ = parse_hour_to_dt(fecha, p['hora_recogida'])
            dt_end = dt + timedelta(minutes=30)
            print(f"Creando: 🏠 RECOGIDA: {hermandad} ({dt.strftime('%d/%m %H:%M')})")
            run_gog([
                "calendar", "create", CALENDAR_ID,
                "--summary", f"🏠 RECOGIDA: {hermandad}",
                "--from", format_dt(dt),
                "--to", format_dt(dt_end),
                "--description", f"{hermandad} regresa a su sede",
                "--location", sede
            ])
            eventos_creados += 1
    
    print(f"\n🎉 Total: {eventos_creados} eventos creados en {CALENDAR_ID}")

if __name__ == '__main__':
    main()
