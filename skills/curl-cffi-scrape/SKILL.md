---
name: curl-cffi-scrape
description: Scraping de webs con protección anti-bot (Cloudflare, DataDome, PerimeterX) usando curl_cffi con TLS fingerprint impersonation.
---

# curl-cffi-scrape — Anti-Bot Web Scraper

Usa `curl_cffi` para imitar el fingerprint TLS/JA3/HTTP2 de Chrome o Edge real, bypassing la mayoría de protecciones anti-bot sin necesidad de browser automation completo.

## Cuándo usar esta skill

| Herramienta | Velocidad | JS Rendering | Anti-Bot TLS | Mejor para |
|---|---|---|---|---|
| **curl_cffi** | ⚡⚡⚡⚡ | ❌ | ✅✅✅✅ | LinkedIn, webs con Cloudflare/SeniorGrove, APIs protegidas |
| **web_fetch (Tavily)** | ⚡⚡⚡ | ❌ | ✅ | Búsquedas, noticias, webs simples |
| **Obscura** | ⚡⚡ | ✅ | ✅✅ | Webs con JavaScript dinámico, captchas simples |
| **catastro** | ⚡⚡⚡⚡ | ❌ | N/A | Datos catastrales oficiales |

**Usar curl_cffi cuando:**
- Tavily devuelve contenido vacío o truncado
- Obscura se queda colgado o muestra CAPTCHA wall
- Necesitas velocidad (no hay JS que renderizar)
- La web usa TLS fingerprinting (la mayoría de anti-bots)

## Script

```bash
python3 /home/gerion/.openclaw/workspace/skills/curl-cffi-scrape/scripts/curl_cffi_scrape.py <url> [opciones]
```

## Opciones

| Opción | Descripción |
|---|---|
| `--text` | Extrae texto limpio (sin HTML tags) |
| `--json` | Interpreta respuesta como JSON |
| `--headers` | Muestra solo headers HTTP |
| `--extract KEYWORD` | Extrae sección alrededor de una keyword |
| `--max-chars N` | Limita output a N caracteres |
| `--browser NAME` | Browser a impersonar (default: chrome120) |
| `--timeout N` | Timeout en segundos (default: 30) |
| `--list-browsers` | Lista browsers disponibles |

## Browsers disponibles

**Chrome:** `chrome110`, `chrome116`, `chrome119`, `chrome120`, `chrome121`, `chrome122`, `chrome123`, `chrome124`, `chrome126`

**Edge:** `edge101`, `edge110`, `edge117`, `edge118`, `edge119`, `edge120`, `edge121`, `edge122`, `edge123`, `edge124`

**Safari:** `safari15_3`, `safari15_4`, `safari15_5`, `safari16_0`, `safari16_3`, `safari17_0`, `safari17_2`, `safari17_4`

**Recomendación:** `chrome120` o `edge124` para la mayoría de casos.

## Ejemplos

### Extraer contenido completo como texto
```bash
python3 curl_cffi_scrape.py "https://www.linkedin.com/posts/..." --text
```

### Buscar una keyword específica
```bash
python3 curl_cffi_scrape.py "https://www.linkedin.com/posts/..." --extract "Jim Simons" --max-chars 3000
```

### Ver headers (útil para debug)
```bash
python3 curl_cffi_scrape.py "https://www.example.com" --headers
```

### API call
```bash
python3 curl_cffi_scrape.py "https://api.example.com/data" --json
```

### Con browser específico
```bash
python3 curl_cffi_scrape.py "https://www.example.com" --text --browser edge124
```

## Ejemplo de uso en código Python

```python
from curl_cffi import requests

r = requests.get(
    "https://www.linkedin.com/posts/...",
    impersonate='chrome120',
    timeout=30,
    headers={
        'Accept-Language': 'en-US,en;q=0.9',
    }
)
print(r.status_code)
print(r.text[:2000])
```

## Webs que funciona bien

- ✅ LinkedIn (posts públicos, perfiles)
- ✅ Webs con Cloudflare generic protection
- ✅ SeniorGrove / anti-bot TLS
- ✅ La mayoría de news sites
- ✅ APIs protegidas con fingerprint

## Webs que NO funciona

- ❌ Idealista (usa DataDome con browser fingerprint, no solo TLS)
- ❌ Webs con CAPTCHA interactivo (tipo Cloudflare challenge)
- ❌ Webs que requieren login real (no bypassea autenticación)

## Notas

- `curl_cffi` ya está instalado en el sistema
- Mucho más rápido que Obscura porque no lanza browser
- Si `--text` devuelve < 200 chars, probablemente es un anti-bot wall
- Combinar con `--extract` para obtener solo lo relevante
