# MEMORY.md

## Gerion (yo)

- **Nombre:** Gerion
- **Emoji:** 🧉
- **Vibe:** Directo, competente, un poco sarcástico, energía "vale"

## Preferencias del usuario

- **Nombre:** Paduel
- **Idioma:** Dirigirse siempre en español de España
- **No usar chino (caracteres chinos como 的话题) en absoluto** — Paduel puede leer inglés pero no chino
- **No usar el emoji de mate 🧉 ni referencias al mate** — Paduel es de Andalucía y le molesta

## Cuenta de Google (Agente)

- **Email:** animagerion@gmail.com
- **Tipo:** Cuenta dedicada para el agente (NO es la cuenta personal de Paduel)
- **Uso:** Es la cuenta que debo usar cuando Paduel diga "mi email", "mi drive", "mi calendario", etc.
- **Credenciales gogcli:** Configuradas en ~/.config/gogcli/ y ~/.config/gog/
- **Token guardado** con GOG_KEYRING_PASSWORD="gerion-gog-2026"

## GitHub

- **Mi GitHub (animagerion):** https://github.com/animagerion/openclaw-workspace-test
- **Tu GitHub (paduel):** https://github.com/paduel

## MiniMax

- **Modelo actual:** MiniMax M2.7
- **Plan:** 1.500 llamadas por ventana de 5h (rolling), semanal ilimitado
- **API endpoint:** `https://platform.minimax.io/v1/api/openplatform/coding_plan/remains`
- **API key:** en `auth-profiles.json` → `profiles.minimax:default.key`
- **Skill:** `skills/minimax-usage/check_usage.sh`

## Búsqueda Web (Tavily)

- **Skill:** `skills/openclaw-tavily-search/` — instalado 2026-04-19
- **API key:** en `~/.openclaw/.env` → `TAVILY_API_KEY`
- **Parámetros clave:** `--topic` (general/news/finance) y `--time-range` (day/week/month/year)
- **Documentación:** https://docs.tavily.com/documentation/integrations/openclaw
- **Script:** `skills/openclaw-tavily-search/scripts/tavily_search.py`
- **Límite:** 1000 búsquedas/mes gratis

## Crons activos

- **08:00** — Agenda diaria (hoy + mañana) → Telegram
- **09:00** — Santos diarios
- **Cada 30 min** — Check Gmail (solo notifica si hay nuevos)
- **Cada 6h** — Auto-commit workspace (solo si hay cambios)
- **Clima Utrera 07:30** — Deshabilitada (timeout por falta de credits)

## Catastro CLI

- **CLI básico:** `/home/gerion/.local/bin/catastro` (API, rápido)
- **CLI completo:** `/home/gerion/.local/bin/catastro_full` (API + scraping web, incluye parcela)
- **Skill:** `skills/catastro/SKILL.md`
- **Uso:** `catastro_full <provincia> <municipio> <calle> [numero]`
- **API:** Oficial del Catastro (ovc.catastro.meh.es) — gratuita, sin certificado
- **Scraping:** sedecatastro.gob.es para superficie parcela y construcciones detalladas
- **Devuelve:** Todo + **superficie parcela** (dato que la API no da)
- **Bug conocido:** Provincia Córdoba (code 14) da 500 en ConsultaMunicipio. Usar "CORDOBA" sin acento

## Gráficos Financieros (Comando "Fibo")

- **Script:** `/home/gerion/.openclaw/workspace/fibo_chart.py`
- **Uso:** `python3 fibo_chart.py <TICKER> [FECHA_INICIO] [FECHA_FIN]`
- **Por defecto:** Si no se pasa fecha, usa 2 años atrás
- **Importante:** El script guarda los gráficos en `/tmp/` (directorio permitido para enviar medios por Telegram)
- **Cuando el usuario pida "Fibo" o "Fibo+":**
  1. Ejecutar el script con el ticker indicado (o sin especificar para 2 años por defecto)
  2. Generar gráfico con: Bollinger Bands, Fibonacci, SMA90, SMA200, MACD, RSI, Volumen
  3. Enviar siempre por Telegram usando la ruta `/tmp/<TICKER>_chart.png`
