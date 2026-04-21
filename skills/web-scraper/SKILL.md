# Web Scraper Skill

Usa Tavily para búsquedas rápidas y Obscura para scraping avanzado con JavaScript.

## Herramientas

- **Tavily** (`skills/openclaw-tavily-search/`): Para búsquedas y consultas simples
- **Obscura**: Headless browser en Rust para web scraping con JS rendering

## Cuándo usar cada uno

| Caso | Herramienta |
|------|-------------|
| Búsqueda web, noticias, info general | Tavily |
| Consultar URLs específicas | Tavily (`--search` mode) |
| Webs que requieren JavaScript | Obscura |
| Extracción de contenido dinámico | Obscura |
| Scraping con evitación de detección | Obscura `--stealth` |

## Comandos Obscura

```bash
# Fetch básico (HTML renderizado)
obscura fetch <url> --dump html

# Extraer texto
obscura fetch <url> --dump text

# Extraer links
obscura fetch <url> --dump links

# Con JavaScript rendered (espera network idle)
obscura fetch <url> --wait-until networkidle0 --dump html

# Modo stealth (anti-detección)
obscura fetch <url> --stealth --dump html

# Evaluar JS custom
obscura fetch <url> --eval "document.querySelector('h1').textContent"

# Servir como CDP server (para Puppeteer/Playwright)
obscura serve --port 9222 --stealth
```

## Ejemplo de uso en prompt

```
Usa Obscura para hacer scraping de [URL]. Extrae el contenido HTML completo
con JavaScript renderizado: obscura fetch [URL] --wait-until networkidle0 --dump html
```

## Notas

- Obscura está en `~/.local/bin/obscura`
- No necesita Chrome ni Node.js
- Modo stealth bloquea trackers y randomiza fingerprint
- Compatible con Puppeteer y Playwright via CDP (puerto 9222)