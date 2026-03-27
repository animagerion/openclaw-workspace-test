#!/usr/bin/env python3
"""
AI News Digest — Recopilador RSS
Descarga artículos de fuentes AI y los guarda en articles.md
"""
import feedparser
import html
from datetime import datetime, timedelta
from urllib.request import urlopen
from urllib.error import URLError
import sys

SOURCES = [
    ("Hacker News AI", "https://hnrss.org/newest?q=AI"),
    ("arXiv cs.AI", "https://rss.arxiv.org/rss/cs.AI"),
    ("TechCrunch AI", "https://techcrunch.com/category/artificial-intelligence/feed/"),
    ("VentureBeat AI", "https://venturebeat.com/ai/feed/"),
    ("机器之心 jiqizhixin", "https://aikai.app/feed"),
    ("量子位 qubit", "https://qubit.cn/feed"),
]

DAYS_AGO = 2
CUTOFF = datetime.utcnow() - timedelta(days=DAYS_AGO)

def clean(text):
    if not text:
        return ""
    text = html.unescape(text)
    text = ' '.join(text.split())
    return text.strip()

def fetch_feed(name, url):
    entries = []
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries[:15]:
            published = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                try:
                    published = datetime(*entry.published_parsed[:6])
                except Exception:
                    pass
            if published and published < CUTOFF:
                continue
            entries.append({
                "title": clean(entry.get('title', '')),
                "url": entry.get('link', ''),
                "summary": clean(entry.get('summary', entry.get('description', '')))[:300],
                "source": name,
                "published": published.strftime('%Y-%m-%d') if published else '?',
            })
    except Exception as e:
        print(f"  ⚠ Error fetching {name}: {e}", file=sys.stderr)
    return entries

all_articles = []
print("📡 Recopilando noticias AI...")
for name, url in SOURCES:
    print(f"  → {name}")
    entries = fetch_feed(name, url)
    all_articles.extend(entries)
    print(f"    {len(entries)} artículos nuevos")

# Deduplicate by URL
seen = set()
unique = []
for a in all_articles:
    if a['url'] not in seen:
        seen.add(a['url'])
        unique.append(a)

# Sort by source priority (Hacker News, arxiv, then rest)
SOURCE_ORDER = {s[0]: i for i, s in enumerate(SOURCES)}
unique.sort(key=lambda x: SOURCE_ORDER.get(x['source'], 99))

print(f"\n✅ Total: {len(unique)} artículos únicos")

# Write articles.md
output = f"""# AI News Digest — {datetime.utcnow().strftime('%Y-%m-%d')}

## Fuentes
- Hacker News (AI)
- arXiv cs.AI
- TechCrunch AI
- VentureBeat AI
- 机器之心 (jiqizhixin)
- 量子位 (qubit)

---

"""
for i, a in enumerate(unique, 1):
    output += f"""### {i}. [{a['title']}]({a['url']})
- **Fuente:** {a['source']} | **Fecha:** {a['published']}
- **Resumen:** {a['summary']}

---
"""

with open("/home/gerion/.openclaw/workspace/skills/ai-news-digest/articles.md", "w") as f:
    f.write(output)

print(f"💾 Guardado en articles.md")
