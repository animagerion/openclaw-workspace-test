# MEMORY.md

## Preferencias del usuario

- **Nombre:** Paduel
- **Idioma:** Dirigirse siempre en español de España

## Cuenta de Google

- **Email principal:** animagerion@gmail.com
- **Servicios configurados:** Gmail, Google Drive, Google Calendar
- Esta es la cuenta que debo usar cuando el usuario pida revisar "mi email", "mi drive", "mi calendario", etc.

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
