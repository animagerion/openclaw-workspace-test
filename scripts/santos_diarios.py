#!/usr/bin/env python3
"""Santos Diarios - Fuente: Wikipedia deaths section"""
import sys, json, re, subprocess, os
from datetime import date

today = date.today()
DAY = f"{today.day:02d}"
MONTH = f"{today.month:02d}"

MESES = {
    "01": "enero", "02": "febrero", "03": "marzo", "04": "abril",
    "05": "mayo", "06": "junio", "07": "julio", "08": "agosto",
    "09": "septiembre", "10": "octubre", "11": "noviembre", "12": "diciembre"
}
MONTH_NAME = MESES[MONTH]
MONTH_EN = today.strftime("%B")

# Fetch Wikipedia
url = f"https://en.wikipedia.org/w/api.php?action=parse&page={MONTH_EN}_{int(DAY)}&prop=text&formatversion=2&format=json&redirects=1"
r = subprocess.run(['curl', '-s', '--max-time', '15', url, '-H', 'User-Agent: Mozilla/5.0'],
                   capture_output=True, text=True)

try:
    d = json.loads(r.stdout)
except:
    sys.exit(0)

t = d.get('parse', {}).get('text', '')
if not t:
    sys.exit(0)

# Buscar seccion Deaths
idx = t.find('Deaths')
if idx < 0:
    sys.exit(0)

section = t[idx:idx+6000]
# Limpiar HTML
section = re.sub(r'<ref[^>]*>.*?</ref>', '', section, flags=re.DOTALL)
section = re.sub(r'<[^>]+>', ' ', section)
section = re.sub(r'&#\d+;', ' ', section)
section = re.sub(r'&[a-z#]+;', ' ', section)
section = re.sub(r'\s+', ' ', section).strip()

# Buscar Pre-1600
pre_idx = section.find('Pre-1600')
if pre_idx >= 0:
    section = section[pre_idx:pre_idx+3000]

# Extraer saints
names = re.findall(r'(?:Saint|Beato|Blessed)\s+([A-Z][a-z]+(?:[\s][A-Z][a-z]+){0,2})', section)

# Deduplicar
seen = set()
clean = []
for n in names:
    n = n.strip()
    n = re.sub(r',.*', '', n).strip()
    if len(n) > 2 and n.lower() not in seen:
        seen.add(n.lower())
        clean.append(n)

TRAD = {
    'George': 'San Jorge', 'Francis': 'San Francisco', 'Mark': 'San Marcos',
    'Luke': 'San Lucas', 'Matthew': 'San Mateo', 'John': 'San Juan',
    'Peter': 'San Pedro', 'Paul': 'San Pablo', 'James': 'Santiago',
    'Michael': 'San Miguel', 'Joseph': 'San Jose', 'Mary': 'Santa Maria',
    'Patrick': 'San Patricio', 'Andrew': 'San Andres', 'Thomas': 'Santo Tomas',
    'Bartholomew': 'San Bartolome', 'Philip': 'San Felipe', 'Simon': 'San Simon',
    'Stephen': 'San Esteban', 'Lawrence': 'San Lorenzo', 'Vincent': 'San Vicente',
    'Augustine': 'San Augustin', 'Benedict': 'San Benito', 'Catherine': 'Santa Catalina',
    'Teresa': 'Santa Teresa', 'Clare': 'Santa Clara', 'Nicholas': 'San Nicolas',
    'Anthony': 'San Antonio', 'Martin': 'San Martin', 'Jerome': 'San Jeronimo',
    'Ignatius': 'San Ignacio', 'Dominic': 'Santo Domingo', 'Rita': 'Santa Rita',
    'Monica': 'Santa Monica', 'Bernadette': 'Santa Bernadette', 'Adalbert': 'San Adelberto',
    'Gerard': 'San Gerardo', 'Ursula': 'Santa Ursula', 'Eulalia': 'Santa Eulalia',
    'Genoveva': 'Santa Genoveva', 'Martial': 'San Marcial', 'George of Lydda': 'San Jorge',
}

msg = f"Santos del {DAY} de {MONTH_NAME}:\n\n"
for name in clean[:8]:
    trad = TRAD.get(name, f"San {name}" if len(name) > 3 else name)
    msg += f"• {trad}\n"

print(msg.strip())
