#!/usr/bin/env python3
"""
curl_cffi web scraper —绕过反爬虫的TLS指纹检查

使用 curl_cffi 模拟真实浏览器的 TLS/JA3/HTTP2 指纹，
可以访问被 Cloudflare、DataDome、PerimeterX 等保护的网站。

用法:
    python3 curl_cffi_scrape.py <url> [--text] [--json] [--headers] [--timeout N]
    python3 curl_cffi_scrape.py <url> --extract "<keyword>" [--max-chars N]

Ejemplos:
    # Extraer contenido completo como texto
    python3 curl_cffi_scrape.py "https://www.linkedin.com/posts/..." --text

    # Extraer solo secciones que contengan una palabra clave
    python3 curl_cffi_scrape.py "https://www.example.com" --extract "Jim Simons"

    # Ver headers de respuesta
    python3 curl_cffi_scrape.py "https://www.example.com" --headers

    # JSON API call
    python3 curl_cffi_scrape.py "https://api.example.com/data" --json

    # Con keyword search
    python3 curl_cffi_scrape.py "https://www.linkedin.com/posts/..." --extract "Markov" --max-chars 3000

Browsers disponibles para impersonate:
    chrome110, chrome116, chrome119, chrome120, chrome121, chrome122, chrome123, chrome124
    chrome126, edge101, edge110, edge117, edge118, edge119, edge120, edge121, edge122, edge123, edge124
    safari15_3, safari15_4, safari15_5, safari16_0, safari16_3, safari17_0, safari17_2, safari17_4
"""

import argparse
import json
import re
import sys
from urllib.parse import urlparse

try:
    from curl_cffi import requests as curl_requests
    IMPERSONATE_BROWSERS = ['chrome110', 'chrome116', 'chrome119', 'chrome120', 'chrome121',
                            'chrome122', 'chrome123', 'chrome124', 'chrome126',
                            'edge101', 'edge110', 'edge117', 'edge118', 'edge119',
                            'edge120', 'edge121', 'edge122', 'edge123', 'edge124',
                            'safari15_3', 'safari15_4', 'safari15_5', 'safari16_0',
                            'safari16_3', 'safari17_0', 'safari17_2', 'safari17_4']
except ImportError:
    print("ERROR: curl_cffi no instalado. Ejecuta: pip3 install curl_cffi", file=sys.stderr)
    sys.exit(1)


DEFAULT_BROWSER = 'chrome120'
TIMEOUT = 30


def clean_html(text):
    """Limpia HTML básico y normaliza espacios."""
    if not text:
        return ''
    # Remove scripts and style blocks
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def fetch_url(url, browser=DEFAULT_BROWSER, timeout=TIMEOUT, headers=None):
    """Hace GET request con impersonation de browser."""
    default_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9,es;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
    }
    if headers:
        default_headers.update(headers)

    try:
        r = curl_requests.get(
            url,
            impersonate=browser,
            timeout=timeout,
            headers=default_headers,
            allow_redirects=True
        )
        return r
    except Exception as e:
        print(f"ERROR fetching {url}: {e}", file=sys.stderr)
        return None


def extract_by_keyword(text, keyword, max_chars=2000):
    """Extrae contexto alrededor de una keyword."""
    lower_text = text.lower()
    lower_kw = keyword.lower()
    idx = lower_text.find(lower_kw)
    if idx == -1:
        return None
    start = max(0, idx - 200)
    end = min(len(text), idx + max_chars)
    return text[start:end]


def extract_structured_data(text):
    """Intenta extraer datos estructurados (JSON-LD, microdata)."""
    results = {}

    # JSON-LD
    jsonld = re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', text, re.DOTALL | re.IGNORECASE)
    if jsonld:
        try:
            results['jsonld'] = json.loads(jsonld[0])
        except Exception:
            results['jsonld_raw'] = jsonld[0][:500]

    # Open Graph
    og = {}
    for match in re.finditer(r'<meta[^>]+property=["\']og:([^"\']+)["\'][^>]+content=["\']([^"\']+)["\']', text, re.IGNORECASE):
        og[match.group(1)] = match.group(2)
    if og:
        results['opengraph'] = og

    # Twitter cards
    tw = {}
    for match in re.finditer(r'<meta[^>]+name=["\']twitter:([^"\']+)["\'][^>]+content=["\']([^"\']+)["\']', text, re.IGNORECASE):
        tw[match.group(1)] = match.group(2)
    if tw:
        results['twitter'] = tw

    return results


def scrape(url, text_mode=False, json_mode=False, headers_mode=False,
           keyword=None, max_chars=2000, browser=DEFAULT_BROWSER):
    """Scrape principal con múltiples modos de salida."""
    r = fetch_url(url, browser=browser)
    if not r:
        sys.exit(1)

    print(f"Status: {r.status_code}", file=sys.stderr)
    print(f"URL final: {r.url}", file=sys.stderr)
    print(f"Content-Type: {r.headers.get('Content-Type', 'unknown')}", file=sys.stderr)
    print(f"Tamaño: {len(r.content)} bytes", file=sys.stderr)
    print("---", file=sys.stderr)

    if headers_mode:
        print(json.dumps(dict(r.headers), indent=2, ensure_ascii=False))
        return

    if json_mode:
        try:
            print(json.dumps(r.json(), indent=2, ensure_ascii=False))
        except Exception:
            print("Response no es JSON válido")
            print(r.text[:1000])
        return

    text = r.text

    if keyword:
        result = extract_by_keyword(text, keyword, max_chars)
        if result:
            print(result)
        else:
            print(f"Keyword '{keyword}' no encontrada")
            sys.exit(1)
        return

    if text_mode:
        # Modo texto limpio
        cleaned = clean_html(text)
        # Si es HTML con poco texto, puede que sea un wall — avisar
        if len(cleaned) < 200:
            print("ADVERTENCIA: Contenido muy corto, puede ser un anti-bot wall", file=sys.stderr)
            print(cleaned)
        else:
            print(cleaned[:max_chars] if max_chars else cleaned)
        return

    # Default: raw text truncado
    print(text[:max_chars] if max_chars else text)


def main():
    parser = argparse.ArgumentParser(
        description='Web scraper con curl_cffi — TLS fingerprint impersonation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('url', help='URL a scrapear')
    parser.add_argument('--text', action='store_true', help='Extraer como texto limpio (sin HTML)')
    parser.add_argument('--json', action='store_true', help='Interpretar response como JSON')
    parser.add_argument('--headers', action='store_true', help='Mostrar solo headers de respuesta')
    parser.add_argument('--extract', metavar='KEYWORD', help='Extraer sección con keyword')
    parser.add_argument('--max-chars', type=int, default=0,
                        help='Máximo caracteres a输出的 (0=sin límite, default=0)')
    parser.add_argument('--timeout', type=int, default=TIMEOUT, help=f'Timeout en segundos (default: {TIMEOUT})')
    parser.add_argument('--browser', default=DEFAULT_BROWSER,
                        help=f'Browser a impersonar (default: {DEFAULT_BROWSER})')
    parser.add_argument('--list-browsers', action='store_true', help='Listar browsers disponibles')

    args = parser.parse_args()

    if args.list_browsers:
        print("Browsers disponibles para impersonation:")
        for b in IMPERSONATE_BROWSERS:
            print(f"  {b}")
        return

    scrape(
        url=args.url,
        text_mode=args.text,
        json_mode=args.json,
        headers_mode=args.headers,
        keyword=args.extract,
        max_chars=args.max_chars if args.max_chars > 0 else 0,
        browser=args.browser
    )


if __name__ == '__main__':
    main()
