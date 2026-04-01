#!/usr/bin/env python3
"""
Recopilador de noticias del día desde fuentes RSS.
Descarga y parsea múltiples fuentes RSS, organiza por categoría,
y genera un archivo markdown con las noticias del día.
"""

import os
import sys
import json
import time
import feedparser
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

# ─── Fuentes RSS ────────────────────────────────────────────────────
SOURCES = {
    'internacional': [
        {
            'name': 'Reuters Top News',
            'url': 'https://feeds.reuters.com/reuters/topNews',
            'lang': 'en',
        },
        {
            'name': 'AP News',
            'url': 'https://apnews.com/rss',
            'lang': 'en',
        },
        {
            'name': 'BBC World',
            'url': 'https://feeds.bbci.co.uk/news/world/rss.xml',
            'lang': 'en',
        },
        {
            'name': 'The Guardian World',
            'url': 'https://www.theguardian.com/world/rss',
            'lang': 'en',
        },
    ],
    'europa': [
        {
            'name': 'Le Monde International',
            'url': 'https://www.lemonde.fr/international/rss_full.xml',
            'lang': 'fr',
        },
        {
            'name': 'El País Internacional',
            'url': 'https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/internacional/portada',
            'lang': 'es',
        },
    ],
    'espana': [
        {
            'name': 'El País España',
            'url': 'https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/espana/portada',
            'lang': 'es',
        },
        {
            'name': 'El Mundo',
            'url': 'https://www.elmundo.es/elmundo/hemeroteca/rss/portada.xml',
            'lang': 'es',
        },
        {
            'name': 'ABC',
            'url': 'https://www.abc.es/rss/feeds/abcPortada.xml',
            'lang': 'es',
        },
        {
            'name': 'La Vanguardia',
            'url': 'https://www.lavanguardia.com/rss/home.xml',
            'lang': 'es',
        },
        {
            'name': 'El Confidencial',
            'url': 'https://www.elconfidencial.com/feeds/latest/',
            'lang': 'es',
        },
        {
            'name': 'elDiario.es',
            'url': 'https://www.eldiario.es/rss/',
            'lang': 'es',
        },
        {
            'name': 'Público',
            'url': 'https://www.publico.es/rss/',
            'lang': 'es',
        },
    ],
    'economia': [
        {
            'name': 'Financial Times',
            'url': 'https://www.ft.com/?format=rss',
            'lang': 'en',
        },
        {
            'name': 'Bloomberg Markets',
            'url': 'https://feeds.bloomberg.com/markets/news.rss',
            'lang': 'en',
        },
        {
            'name': 'Expansión',
            'url': 'https://e00-elmundo.uecdn.es/expansion/rss/expansionPortada.xml',
            'lang': 'es',
        },
    ],
}

CACHE_FILE = '/tmp/news_cache.json'
CACHE_HOURS = 3


def load_cache():
    """Carga el caché si es reciente."""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE) as f:
                cache = json.load(f)
            cache_time = datetime.fromisoformat(cache.get('timestamp', '2000-01-01'))
            if datetime.now() - cache_time < timedelta(hours=CACHE_HOURS):
                print(f"[CACHE] Usando caché de {cache_time.strftime('%H:%M')}")
                return cache
        except Exception:
            pass
    return None


def save_cache(news_data):
    """Guarda los resultados en caché."""
    cache = {
        'timestamp': datetime.now().isoformat(),
        'news': news_data,
    }
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def fetch_feed(source, delay=2):
    """Descarga un feed RSS con delay."""
    name = source['name']
    url = source['url']
    try:
        print(f"  Descargando: {name}...", end='', flush=True)
        feed = feedparser.parse(url)
        time.sleep(delay)

        if feed.bozo and not feed.entries:
            print(f" ERROR (feed vacío)")
            return []

        entries = []
        for entry in feed.entries[:15]:
            # Extraer fecha de publicación
            pub_date = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                try:
                    pub_date = datetime(*entry.published_parsed[:6])
                except Exception:
                    pass

            # Extraer descripción/summary
            summary = ''
            if hasattr(entry, 'summary'):
                summary = entry.summary
            elif hasattr(entry, 'description'):
                summary = entry.description
            # Limpiar HTML del summary
            import re
            summary = re.sub(r'<[^>]+>', '', summary).strip()
            if len(summary) > 400:
                summary = summary[:400] + '...'

            # Extraer enlace
            link = ''
            if hasattr(entry, 'link'):
                link = entry.link

            entries.append({
                'title': entry.get('title', '').strip(),
                'summary': summary,
                'link': link,
                'pub_date': pub_date.isoformat() if pub_date else None,
                'source': name,
                'lang': source['lang'],
            })

        print(f" OK ({len(entries)} noticias)")
        return entries

    except Exception as e:
        print(f" ERROR: {e}")
        return []


def is_recent_news(entry, hours=36):
    """Determina si una noticia es reciente (últimas horas)."""
    if not entry.get('pub_date'):
        return True  # Si no hay fecha, incluir por seguridad
    try:
        pub = datetime.fromisoformat(entry['pub_date'])
        age = datetime.now() - pub
        return age < timedelta(hours=hours)
    except Exception:
        return True


def deduplicate(news_list):
    """Elimina noticias duplicadas basándose en título similar."""
    seen = set()
    unique = []
    for item in news_list:
        # Crear clave normalizada del título
        title_key = item['title'].lower()
        title_key = ''.join(c for c in title_key if c.isalnum() or c.isspace())
        title_key = ' '.join(title_key.split())[:80]

        if title_key not in seen:
            seen.add(title_key)
            unique.append(item)
    return unique


def collect_news(use_cache=True):
    """Recopila noticias de todas las fuentes."""
    print(f"\n{'='*60}")
    print(f"Boletn de Noticias — {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"{'='*60}\n")

    all_news = defaultdict(list)

    if use_cache:
        cache = load_cache()
        if cache:
            print("[CACHE HIT] Devolviendo noticias en caché")
            return cache['news']

    for category, sources in SOURCES.items():
        print(f"\n[{category.upper()}]")
        for source in sources:
            entries = fetch_feed(source)
            for entry in entries:
                entry['category'] = category
                all_news[category].append(entry)
            time.sleep(1)  # Delay entre fuentes

    # Filtrar noticias recientes y deduplicar
    print(f"\n\n[PROCESO] Filtrando y deduplicando...")
    for category in all_news:
        # Filtrar recientes
        all_news[category] = [e for e in all_news[category] if is_recent_news(e)]
        # Deduplicar
        all_news[category] = deduplicate(all_news[category])
        # Ordenar por fecha (más recientes primero)
        all_news[category].sort(
            key=lambda x: x.get('pub_date', '2000-01-01'),
            reverse=True
        )
        print(f"  {category}: {len(all_news[category])} noticias nicas")

    # Guardar caché
    save_cache(all_news)
    return all_news


def generate_markdown(news_data):
    """Genera el boletín en formato Markdown."""
    today = datetime.now().strftime('%d de %B de %Y').capitalize()

    md = []
    md.append(f"# BOLETÍN DE NOTICIAS")
    md.append(f"## {today}\n")
    md.append(f"_Recopilado de múltiples fuentes internacionales y españolas_\n")
    md.append("---\n")

    # INTERNATIONAL
    if news_data.get('internacional'):
        md.append("## INTERNACIONAL\n")
        for item in news_data['internacional'][:5]:
            md.append(f"**{item['title']}**")
            md.append(f"_{item['source']}_")
            if item['summary']:
                md.append(f"{item['summary']}")
            if item['link']:
                md.append(f"Fuente: {item['link']}")
            md.append("")

    # EUROPA
    if news_data.get('europa'):
        md.append("---\n## EUROPA\n")
        for item in news_data['europa'][:4]:
            md.append(f"**{item['title']}**")
            md.append(f"_{item['source']}_")
            if item['summary']:
                md.append(f"{item['summary']}")
            if item['link']:
                md.append(f"Fuente: {item['link']}")
            md.append("")

    # ESPAÑA
    if news_data.get('espana'):
        md.append("---\n## ESPAÑA\n")
        for item in news_data['espana'][:5]:
            md.append(f"**{item['title']}**")
            md.append(f"_{item['source']}_")
            if item['summary']:
                md.append(f"{item['summary']}")
            if item['link']:
                md.append(f"Fuente: {item['link']}")
            md.append("")

    # ECONOMÍA
    if news_data.get('economia'):
        md.append("---\n## ECONOMÍA Y MERCADOS\n")
        for item in news_data['economia'][:4]:
            md.append(f"**{item['title']}**")
            md.append(f"_{item['source']}_")
            if item['summary']:
                md.append(f"{item['summary']}")
            if item['link']:
                md.append(f"Fuente: {item['link']}")
            md.append("")

    md.append("---\n")
    md.append(f"_Boletín generado el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}_\n")

    return '\n'.join(md)


def main():
    parser = argparse.ArgumentParser(description='Recopila noticias del día')
    parser.add_argument('--no-cache', action='store_true', help='Ignorar caché')
    parser.add_argument('--output', '-o', default='/tmp/news_bulletin.md', help='Archivo de salida')
    args = parser.parse_args()

    news = collect_news(use_cache=not args.no_cache)
    md = generate_markdown(news)

    with open(args.output, 'w') as f:
        f.write(md)

    print(f"\n[OK] Boletín guardado en: {args.output}")
    print(f"Noticias totales: {sum(len(v) for v in news.values())}")


if __name__ == '__main__':
    main()
