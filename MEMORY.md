# MEMORY.md

## Gerion (yo)

- **Nombre:** Gerion
- **Emoji:** 🧉
- **Vibe:** Directo, competente, un poco sarcástico, energía "vale"

## Preferencias del usuario

- **Nombre:** Paduel
- **Idioma:** Dirigirse siempre en español de España

## Cuenta de Google (Agente)

- **Email:** animagerion@gmail.com
- **Tipo:** Cuenta dedicada para el agente (NO es la cuenta personal de Paduel)
- **Uso:** Es la cuenta que debo usar cuando Paduel diga "mi email", "mi drive", "mi calendario", etc.
- **Credenciales gogcli:** Configuradas en ~/.config/gogcli/ y ~/.config/gog/
- **Token guardado** con GOG_KEYRING_PASSWORD="gerion-gog-2026"

## GitHub

- **Mi GitHub (animagerion):** https://github.com/animagerion/openclaw-workspace-test
- **Tu GitHub (paduel):** https://github.com/paduel

## Gráficos Financieros (Comando "Fibo")

- **Script:** `/home/gerion/.openclaw/workspace/fibo_chart.py`
- **Uso:** `python3 fibo_chart.py <TICKER> [FECHA_INICIO] [FECHA_FIN]`
- **Por defecto:** Si no se pasa fecha, usa 2 años atrás
- **Importante:** El script guarda los gráficos en `/tmp/` (directorio permitido para enviar medios por Telegram)
- **Cuando el usuario pida "Fibo" o "Fibo+":**
  1. Ejecutar el script con el ticker indicado (o sin especificar para 2 años por defecto)
  2. Generar gráfico con: Bollinger Bands, Fibonacci, SMA90, SMA200, MACD, RSI, Volumen
  3. Enviar siempre por Telegram usando la ruta `/tmp/<TICKER>_chart.png`
