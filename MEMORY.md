# MEMORY.md

## Gerion (yo)

- **Nombre:** Gerion
- **Emoji:** 🧉
- **Vibe:** Directo, competente, un poco sarcástico, energía "vale"

## Reglas de Backtesting (CRÍTICO)

**ANTISESGO: No usar datos futuros para entrenar modelos.**

Esta regla es inviolable. Siempre que haga un backtest:
- **NUNCA** entrenar con toda la serie y luego testar en los mismos datos
- Usar **walk-forward**: entrenar con datos hasta T-1, testar en T
- O usar otra técnica sin look-ahead bias
- Si no sé cómo hacerlo sin sesgo, PREGUNTAR antes de ejecutar

Esto se aplica a cualquier modelo: HMM, ML, regresión, etc.

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

## Vocabulario Arquitectura Código (Matt Pocock)

De: https://github.com/mattpocock/skills/blob/main/improve-codebase-architecture/LANGUAGE.md

### Conceptos clave
- **Module**: cualquier cosa con interface + implementation. Escala-agnóstico (función, clase, package, o slice). No decir "unit" ni "component".
- **Interface**: TODO lo que un caller necesita saber para usar el módulo correctamente — no solo el tipo, también invariants, constraints de orden, modos de error, config necesaria, performance.
- **Implementation**: lo que hay dentro del módulo. Diferente de Adapter: puede haber adapter pequeño con implementación grande (Postgres repo) o adapter grande con implementación pequeña (in-memory fake).
- **Seam**: lugar donde puedes alterar comportamiento sin editar ahí. Es donde vive la interface. No decir "boundary" (overloaded con DDD).
- **Adapter**: cosa concreta que satisface una interface en un seam. Describe rol, no sustancia.
- **Depth (leverage)**: lo que los callers ganan con módulos profundos. Mucha capacidad tras poca interface. Módulo shallow = interface casi tan compleja como la implementación.
- **Locality**: lo que los maintainers ganan con depth. Cambios, bugs, conocimiento y verificación se concentran en un lugar.

### Principios operativos
- Depth es propiedad de la interface, no de la implementación
- **Deletion test**: si borras el módulo y la complejidad desaparece → no ocultaba nada. Si la complejidad reaparece en N callers → ganaba su sitio
- La interface es la superficie de test. Callers y tests cruzan el mismo seam
- **"One adapter = hypothetical seam. Two adapters = real seam"** → no crear seams prematuras
- No introducir seam a menos que algo realmente varie entre adaptadores

### Para qué nos sirve a nosotros
- **Depth como leverage**: cuando Paduel me pide algo, dar solución completa (con herramientas, contexto) > dar solo lo que pide (shallow)
- **Deletion test** analog: cuando creo algo (script, cron, deck), pensar si realmente oculta complejidad o solo la mueve
- Para evaluar si una automatización merece existir como módulo o es demasiado thin

### Lo que NO nos sirve
- Es vocabulario para revisión de arquitectura de código, no para nuestro workflow
- No lo necesitamos formalizar
