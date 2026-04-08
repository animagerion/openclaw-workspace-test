#!/bin/bash
cd /home/gerion/.openclaw/workspace
python3 -c "
import feedparser, html
from datetime import datetime, timedelta
sources = [
    ('HN', 'https://hnrss.org/newest?q=AI'),
    ('TC', 'https://techcrunch.com/category/artificial-intelligence/feed/'),
]
cutoff = datetime.utcnow() - timedelta(days=2)
arts = []
for name, url in sources:
    feed = feedparser.parse(url)
    for e in feed.entries[:10]:
        try:
            p = datetime(*e.published_parsed[:6]) if e.published_parsed else None
        except:
            p = None
        if p and p < cutoff:
            continue
        arts.append({'t': html.unescape(e.get('title','')), 'u': e.get('link',''), 'n': name})
print(len(arts), 'articulos.')
if arts:
    print('Primero:', arts[0]['t'])
"
