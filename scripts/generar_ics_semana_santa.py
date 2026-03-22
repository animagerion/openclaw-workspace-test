#!/usr/bin/env python3
"""
Generar archivo .ics para Semana Santa Utrera 2026
"""
import json
from datetime import datetime, timedelta

def parse_time(time_str):
    """Convertir string de hora a datetime.time"""
    return datetime.strptime(time_str, "%H:%M").time()

def time_to_ics(time_obj, date_obj):
    """Combinar fecha y hora en string ICS (YYYYMMDDTHHMMSS)"""
    dt = datetime.combine(date_obj, time_obj)
    return dt.strftime('%Y%m%dT%H%M%S')

def crear_evento_ics(summary, date, start_time, end_time, description="", location="Utrera", uid=""):
    """Crear un evento en formato ICS"""
    start_dt = datetime.combine(date, start_time)
    
    # Si la hora de fin es menor que la de inicio, es al día siguiente
    if end_time < start_time:
        end_dt = datetime.combine(date + timedelta(days=1), end_time)
    else:
        end_dt = datetime.combine(date, end_time)
    
    dtstamp = datetime.now().strftime('%Y%m%dT%H%M%SZ')
    uid_str = uid if uid else f"{summary.replace(' ', '')}-{date.strftime('%Y%m%d')}-{start_time.strftime('%H%M')}@utrera2026"
    
    event = f"""BEGIN:VEVENT
UID:{uid_str}
DTSTAMP:{dtstamp}
DTSTART:{time_to_ics(start_time, date)}
DTEND:{time_to_ics(end_time, date)}
SUMMARY:{summary}
LOCATION:{location}
DESCRIPTION:{description}
STATUS:CONFIRMED
TRANSP:OPAQUE
END:VEVENT"""
    return event

def main():
    # Leer datos JSON
    with open('/home/gerion/.openclaw/workspace/semana_santa_utrera_2026.json', 'r') as f:
        data = json.load(f)
    
    events = []
    
    for procesion in data['procesiones']:
        hermandad = procesion['hermandad']
        fecha = datetime.strptime(procesion['fecha'], '%Y-%m-%d').date()
        nombre_completo = procesion.get('nombre_completo', hermandad)
        sede = procesion.get('sede', 'Utrera')
        itinerario = procesion.get('itinerario', [])
        
        desc_base = f"Hermandad: {nombre_completo}\\nSede: {sede}"
        if itinerario:
            desc_base += f"\\n\\nItinerario:\\n" + "\\n".join([f"• {p}" for p in itinerario])
        
        # 1. SALIDA
        if procesion.get('hora_salida'):
            hora_salida = parse_time(procesion['hora_salida'])
            hora_fin = (datetime.combine(fecha, hora_salida) + timedelta(minutes=30)).time()
            events.append(crear_evento_ics(
                f"🕯️ SALIDA: {hermandad}",
                fecha,
                hora_salida,
                hora_fin,
                description=desc_base,
                location=sede
            ))
        
        # 2. CARRERA OFICIAL
        for idx, punto in enumerate(itinerario):
            if 'Carrera Oficial' in punto:
                try:
                    hora_str = punto.split('(')[1].split(' ')[0]
                    hora_co = datetime.strptime(hora_str, '%H:%M').time()
                    hora_fin = (datetime.combine(fecha, hora_co) + timedelta(minutes=15)).time()
                    events.append(crear_evento_ics(
                        f"📍 {hermandad} - Carrera Oficial",
                        fecha,
                        hora_co,
                        hora_fin,
                        description=f"{hermandad} pasa por la Carrera Oficial",
                        location="Carrera Oficial, Utrera"
                    ))
                except:
                    pass
        
        # 3. RECOGIDA
        if procesion.get('hora_recogida'):
            hora_recogida = parse_time(procesion['hora_recogida'])
            hora_fin = (datetime.combine(fecha, hora_recogida) + timedelta(minutes=30)).time()
            events.append(crear_evento_ics(
                f"🏠 RECOGIDA: {hermandad}",
                fecha,
                hora_recogida,
                hora_fin,
                description=f"La Hermandad {hermandad} regresa a su sede",
                location=sede
            ))
    
    # Generar archivo ICS
    events_text = "\n".join(events)
    ics_content = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Semana Santa Utrera 2026//ES
CALSCALE:GREGORIAN
METHOD:PUBLISH
X-WR-CALNAME:Semana Santa Utrera 2026
X-WR-TIMEZONE:Europe/Madrid
X-WR-CALDESC:Programa de procesiones y actos de Semana Santa en Utrera 2026
""" + events_text + """
END:VCALENDAR"""
    
    output_path = '/home/gerion/.openclaw/workspace/semana_santa_utrera_2026.ics'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(ics_content)
    
    print(f"✅ Archivo ICS generado: {output_path}")
    print(f"   Total eventos: {len(events)}")

if __name__ == '__main__':
    main()
