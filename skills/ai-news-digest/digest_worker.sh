#!/bin/bash
# AI News Digest Worker - Step 1 (collect & upload raw articles)
# Este script lo ejecuta el cron. El agente redacta el digest después.
export PATH="/home/gerion/.local/bin:$PATH"
export GOG_KEYRING_PASSWORD="gerion-gog-2026"
SKILL_DIR="/home/gerion/.openclaw/workspace/skills/ai-news-digest"
DATE=$(date +%Y-%m-%d)
ARTICLES_FILE="$SKILL_DIR/articles.md"
DIGEST_FILE="$SKILL_DIR/digest_$DATE.md"
DRIVE_FOLDER_ID="13QjL_Sy4_fYG8GY5b8Q5kfOs16z8cIKk"

cd /home/gerion/.openclaw/workspace

echo "📡 Recopilando noticias AI..."

# Recopilar artículos
python3 << 'PYEOF'
import feedparser, html, json
from datetime import datetime, timedelta

sources = [
    ('Hacker News AI', 'https://hnrss.org/newest?q=AI'),
    ('arXiv cs.AI', 'https://rss.arxiv.org/rss/cs.AI'),
    ('TechCrunch AI', 'https://techcrunch.com/category/artificial-intelligence/feed/'),
    ('VentureBeat AI', 'https://venturebeat.com/ai/feed/'),
]

cutoff = datetime.utcnow() - timedelta(days=2)
arts = []

for name, url in sources:
    try:
        feed = feedparser.parse(url)
        for e in feed.entries[:20]:
            try:
                p = datetime(*e.published_parsed[:6]) if e.published_parsed else None
            except:
                p = None
            if p and p < cutoff:
                continue
            summary = e.get('summary', e.get('description', ''))
            arts.append({
                'title': ' '.join(html.unescape(e.get('title', '')).split()),
                'url': e.get('link', ''),
                'summary': ' '.join(html.unescape(summary)[:500].split()),
                'source': name,
                'published': p.strftime('%Y-%m-%d') if p else '?',
            })
    except Exception as ex:
        print(f'Error {name}: {ex}', file=__import__('sys').stderr)

seen = set()
unique = []
for a in arts:
    if a['url'] not in seen:
        seen.add(a['url'])
        unique.append(a)

source_order = {s[0]: i for i, s in enumerate(sources)}
unique.sort(key=lambda x: source_order.get(x['source'], 99))

with open('/home/gerion/.openclaw/workspace/skills/ai-news-digest/articles.md', 'w') as f:
    f.write(f"# AI News — {datetime.utcnow().strftime('%Y-%m-%d')}\n\n")
    f.write(f"## {len(unique)} artículos recopilados\n\n")
    for i, a in enumerate(unique[:40], 1):
        f.write(f"### {i}. {a['title']}\n")
        f.write(f"**Fuente:** {a['source']} | **Fecha:** {a['published']}\n")
        f.write(f"**URL:** {a['url']}\n")
        f.write(f"**Resumen:** {a['summary']}\n\n---\n\n")

print(f'Articulos: {len(unique)}')
PYEOF

# Upload raw articles to Drive
echo "📤 Subiendo a Drive..."
RESULT=$(GOG_KEYRING_PASSWORD="$GOG_KEYRING_PASSWORD" gog drive upload "$ARTICLES_FILE" --parent "$DRIVE_FOLDER_ID" --account animagerion@gmail.com --no-input 2>&1)
FILE_ID=$(echo "$RESULT" | grep -oP 'id\s+\K\S+' | head -1)
DRIVE_LINK=""
if [ -n "$FILE_ID" ]; then
    DRIVE_LINK=$(GOG_KEYRING_PASSWORD="$GOG_KEYRING_PASSWORD" gog drive url "$FILE_ID" --account animagerion@gmail.com --no-input 2>&1 | grep -oP 'https://[^\s]+' | head -1)
fi
echo "Drive: $DRIVE_LINK"

# Create placeholder that the agent will overwrite
echo "# AI News Digest — $DATE" > "$DIGEST_FILE"
echo "# El agente redactará el digest extenso desde articles.md" >> "$DIGEST_FILE"

echo "✅ Step 1 completo. Artículos en Drive."