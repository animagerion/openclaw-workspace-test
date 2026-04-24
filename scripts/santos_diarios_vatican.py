#!/usr/bin/env python3
"""Santos Diarios — Vatican News API → Telegram"""

import json
import sys
from datetime import date
import urllib.request

def fetch_saints():
    today = date.today()
    month = today.strftime("%m")
    day = today.strftime("%d")
    url = f"https://www.vaticannews.va/es/santos/{month}/{day}.saints.js"

    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.9",
        "Accept-Language": "es-ES,es;q=0.9",
        "Referer": "https://www.vaticannews.va/es/santos.html",
    })

    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = resp.read().decode("utf-8")

    raw = raw.strip()
    if raw.startswith("callback("):
        raw = raw[len("callback("):-1]

    data = json.loads(raw)
    return data.get("saints", [])

def format_saints(saints):
    lines = []
    today = date.today()
    lines.append(f"📿 Santos del {today.strftime('%d/%m')}")
    lines.append("")

    for s in saints:
        name = s.get("name", "")
        summary = s.get("summary", "")
        lines.append(f"• {name}")
        if summary:
            lines.append(f"  {summary}")
        lines.append("")

    return "\n".join(lines)

def main():
    saints = fetch_saints()
    if not saints:
        print("No saints found", file=sys.stderr)
        sys.exit(1)

    print(format_saints(saints))

if __name__ == "__main__":
    main()
