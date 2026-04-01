#!/usr/bin/env python3
"""
Property Valuation Scraper — Spain
Estimates property value by scraping Idealista.es for price/m² in a zone,
then multiplying by the catastral built surface.

Usage:
    python3 valuation_scraper.py "Calle Donaires 8, Utrera" 348
    python3 valuation_scraper.py --lat 37.1852 --lon -5.7799 348
    python3 valuation_scraper.py --postal 41710 348

Fallback: If Idealista blocks us (DataDome protection), uses INE/regional
average price/m² as approximate estimate. The result will be clearly
marked as "fallback estimate" in that case.

Cache: Results are stored in /tmp/idealista_cache.json to avoid
re-scraping the same zones within a session.
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

CACHE_FILE = Path("/tmp/idealista_cache.json")

# ---------------------------------------------------------------------------
# Idealista scraping
# ---------------------------------------------------------------------------

# Regional average price/m² (€/m²) by province — fallback data.
# Sourced from INE 2024-2025 reported averages. Used when Idealista is blocked.
INE_FALLBACK_PRICES = {
    # Sevilla province municipalities
    "utrera": 1250,
    "sevilla": 2100,
    "utrera": 1250,
    # Cádiz province
    "cadiz": 1950,
    "jerez de la frontera": 1450,
    "algeciras": 1550,
    # Córdoba province
    "cordoba": 1400,
    "montilla": 1100,
    "lucena": 1200,
    # Málaga province
    "malaga": 2450,
    "marbella": 3200,
    "torremolinos": 2100,
    # Barcelona
    "barcelona": 3800,
    "hospitalet de llobregat": 2500,
    "badalona": 2200,
    # Madrid
    "madrid": 3500,
    "alcala de henares": 2400,
    "fuenlabrada": 2000,
    # Valencia
    "valencia": 2100,
    "alicante": 1950,
    # Default Spain average (INE 2024)
    "default": 1587,
}


def load_cache() -> dict:
    """Load the scraping cache from disk."""
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text())
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_cache(cache: dict) -> None:
    """Persist the cache to disk."""
    CACHE_FILE.write_text(json.dumps(cache, indent=2, ensure_ascii=False))


def get_cache_key(location: str, lat: float = None, lon: float = None) -> str:
    """Build a cache key from location or coordinates."""
    if lat is not None and lon is not None:
        # Round to 3 decimal places (~111m precision)
        return f"lat={round(lat,3)},lon={round(lon,3)}"
    return location.lower().strip()


def idealista_search(location: str, lat: float = None, lon: float = None) -> dict:
    """
    Scrape Idealista search results for a location and extract price/m².

    Returns dict with keys:
        price_per_m2: float (€/m²)
        source: str ("idealista" or "ine_fallback")
        zone: str (zone/postal used)
        listings_count: int
        method: str ("scraped" or "estimated")
    """
    cache = load_cache()
    cache_key = get_cache_key(location, lat, lon)

    # Check cache first
    if cache_key in cache:
        print(f"  [cache hit] Using cached result for '{cache_key}'")
        return cache[cache_key]

    # Try Idealista scrape
    result = _scrape_idealista(location, lat, lon)

    if result.get("method") == "scraped":
        print(f"  [idealista] Scraped price/m²: €{result['price_per_m2']:.0f}/m²")
    else:
        print(f"  [fallback] Idealista blocked — using INE regional average: €{result['price_per_m2']:.0f}/m²")

    # Cache even the fallback so we don't keep hammering
    cache[cache_key] = result
    save_cache(cache)

    return result


def _build_idealista_url(location: str, lat: float = None, lon: float = None) -> str:
    """Build an Idealista search URL from location or coordinates."""
    if lat is not None and lon is not None:
        # Use coordinates-based search
        return f"https://www.idealista.com/s/{lat},{lon}/"
    else:
        # Clean location string for URL
        slug = location.lower().strip()
        slug = re.sub(r"[,\s]+", "-", slug)
        slug = re.sub(r"[^\w\-]", "", slug)
        return f"https://www.idealista.com/s/{slug}/"


def _scrape_idealista(location: str, lat: float = None, lon: float = None) -> dict:
    """
    Attempt to scrape Idealista for price/m² data.
    Returns fallback if blocked by DataDome or on any error.
    """
    url = _build_idealista_url(location, lat, lon)
    zone = f"{lat},{lon}" if lat else location

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;"
            "q=0.9,image/avif,image/webp,*/*;q=0.8"
        ),
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

    try:
        resp = requests.get(url, headers=headers, timeout=15)
    except requests.RequestException as e:
        print(f"  [error] Request failed: {e}")
        return _build_fallback(zone)

    if resp.status_code != 200:
        print(f"  [warn] Idealista returned HTTP {resp.status_code}")
        return _build_fallback(zone)

    # Check for DataDome block
    if "datadome" in resp.text.lower() or "please enable js" in resp.text.lower():
        print(f"  [warn] DataDome protection detected — Idealista blocked")
        return _build_fallback(zone)

    soup = BeautifulSoup(resp.text, "html.parser")

    # Try to find price/m² data on the page
    price_per_m2 = _extract_price_per_m2(soup)

    if price_per_m2:
        return {
            "price_per_m2": price_per_m2,
            "source": "idealista",
            "zone": zone,
            "method": "scraped",
            "url": url,
        }

    # Try to extract from listing cards
    price_per_m2 = _extract_from_listings(soup)
    if price_per_m2:
        return {
            "price_per_m2": price_per_m2,
            "source": "idealista",
            "zone": zone,
            "method": "scraped",
            "url": url,
        }

    print(f"  [warn] Could not extract price/m² from Idealista page")
    return _build_fallback(zone)


def _extract_price_per_m2(soup: BeautifulSoup) -> float | None:
    """Try to find price/m² in Idealista's aggregated stats elements."""
    # Look for elements containing €/m² patterns
    for el in soup.find_all(text=re.compile(r"€/\s*m")):
        # Walk up to get the containing element text
        parent = el.parent
        if parent:
            text = parent.get_text()
            match = re.search(r"([\d.]+)\s*€/\s*m", text)
            if match:
                return float(match.group(1).replace(".", ""))
    return None


def _extract_from_listings(soup: BeautifulSoup) -> float | None:
    """
    Extract price/m² from individual listing cards.
    Idealista shows price and size on each card.
    """
    prices_per_m2 = []

    # Idealista listing cards — various selectors
    cards = soup.select("div[item-card], article.item, .listing-item, div[itemtype*='Residence']")

    for card in cards:
        card_text = card.get_text()

        # Extract price: "145.000 €" or "145,000 €"
        price_match = re.search(r"([\d.,]+)\s*€", card_text)
        if not price_match:
            continue
        price_str = price_match.group(1).replace(".", "").replace(",", "")
        try:
            price = float(price_str)
        except ValueError:
            continue

        # Extract size: "85 m²" or "85m²"
        size_match = re.search(r"([\d.]+)\s*m", card_text)
        if not size_match:
            continue
        try:
            size = float(size_match.group(1))
        except ValueError:
            continue

        if size > 0:
            prices_per_m2.append(price / size)

    if prices_per_m2:
        # Return median to reduce outlier impact
        prices_per_m2.sort()
        median_idx = len(prices_per_m2) // 2
        return prices_per_m2[median_idx]

    return None


def _build_fallback(zone: str) -> dict:
    """Build a fallback result using INE regional averages."""
    # Try to detect province/municipality from zone string
    zone_lower = zone.lower()

    # Match known municipalities
    for key, price in INE_FALLBACK_PRICES.items():
        if key in zone_lower:
            return {
                "price_per_m2": price,
                "source": "ine_fallback",
                "zone": zone,
                "method": "estimated",
            }

    # Default Spain average
    return {
        "price_per_m2": INE_FALLBACK_PRICES["default"],
        "source": "ine_fallback",
        "zone": zone,
        "method": "estimated",
    }


# ---------------------------------------------------------------------------
# Valuation logic
# ---------------------------------------------------------------------------

def estimate_value(price_per_m2: float, surface_m2: float) -> dict:
    """
    Calculate valuation range from price/m² and surface.
    Returns dict with conservative, average, and optimistic estimates.
    """
    avg_value = price_per_m2 * surface_m2

    # ±10% range for conservative/optimistic
    conservative = avg_value * 0.90
    optimistic = avg_value * 1.10

    return {
        "conservative": conservative,
        "average": avg_value,
        "optimistic": optimistic,
    }


def format_currency(amount: float) -> str:
    """Format a number as Spanish euro currency."""
    return f"€{amount:,.0f}".replace(",", ".")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="Estimate property value using Idealista price/m² × surface"
    )
    parser.add_argument(
        "address",
        nargs="?",
        help="Property address (e.g. 'Calle Donaires 8, Utrera')",
    )
    parser.add_argument(
        "surface",
        type=float,
        help="Built surface in m² (from catastral data)",
    )
    parser.add_argument(
        "--lat",
        type=float,
        help="Latitude for location",
    )
    parser.add_argument(
        "--lon",
        type=float,
        help="Longitude for location",
    )
    parser.add_argument(
        "--postal",
        type=str,
        help="Postal code (e.g. '41710')",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Ignore cached results and re-scrape",
    )

    args = parser.parse_args()

    if not args.address and args.lat is None and args.postal is None:
        parser.error("Either provide an address, --lat/--lon, or --postal")

    if args.surface <= 0:
        parser.error("Surface must be a positive number")

    return args


def main():
    args = parse_args()

    print("\n" + "=" * 60)
    print("  PROPERTY VALUATION ESTIMATE")
    print("=" * 60)

    # Determine location input
    if args.lat is not None and args.lon is not None:
        location = f"{args.lat},{args.lon}"
    else:
        location = args.address or args.postal
    print(f"\n  Location : {location}")
    print(f"  Surface : {args.surface:.0f} m² (catastral built surface)")

    # Optionally clear cache
    if args.no_cache and CACHE_FILE.exists():
        CACHE_FILE.unlink()
        print("  [cache] Cleared")

    # Sleep to be polite (Idealista ToS)
    print("\n  [info] Waiting 2s before scraping (polite delay)...")
    time.sleep(2)

    # Get price/m²
    print("\n  [step 1] Fetching price/m² data...")
    price_data = idealista_search(
        location,
        lat=args.lat,
        lon=args.lon,
    )

    price_per_m2 = price_data["price_per_m2"]
    method = price_data["method"]
    source = price_data["source"]

    print(f"\n  Price/m²  : €{price_per_m2:.0f}/m²")
    print(f"  Source    : {'Idealista (scraped)' if method == 'scraped' else 'INE regional average (fallback)'}")
    print(f"  Zone      : {price_data['zone']}")

    # Calculate estimate
    print("\n  [step 2] Calculating valuation...")
    valuation = estimate_value(price_per_m2, args.surface)

    print(f"\n  {'─' * 40}")
    print(f"  VALUATION RESULTS")
    print(f"  {'─' * 40}")
    print(f"  Superficie : {args.surface:.0f} m²")
    print(f"  Precio/m²  : €{price_per_m2:.0f}/m²")
    print(f"  {'─' * 40}")
    print(f"  CONSERVADOR: {format_currency(valuation['conservative'])}")
    print(f"  MEDIA      : {format_currency(valuation['average'])}")
    print(f"  OPTIMISTA  : {format_currency(valuation['optimistic'])}")
    print(f"  {'─' * 40}")

    if method == "estimated":
        print(f"\n  ⚠ NOTA: Estimación basada en media INE regional,")
        print(f"    no en datos de Idealista (bloqueado por scraping).")

    print(f"\n  Source data: {price_data.get('url', 'N/A')}")
    print(f"  Method: {method}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
