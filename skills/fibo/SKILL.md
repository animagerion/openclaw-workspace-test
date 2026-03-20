---
name: fibo
description: Genera gráficos técnicos Fibonacci+ para activos financieros (acciones, ETFs, криптовалюты). Incluye SMA 90/200, Bollinger Bands, MACD, RSI y Volumen.
---

# Fibo CLI — Gráficos Técnicos Fibonacci+

Genera gráficos de análisis técnico con niveles Fibonacci, medias móviles y principales indicadores.

## Ubicación

CLI: `/home/gerion/.local/bin/fibo` (o `fibo` si ~/.local/bin está en PATH)
Script: `/home/gerion/.openclaw/workspace/scripts/fibo_cli.py`

## Uso

### Comando básico

```bash
fibo <TICKER>
```

### Con fechas específicas

```bash
fibo <TICKER> <FECHA_INICIO> [FECHA_FIN]
```

Formato de fecha: `YYYY-MM-DD`

## Ejemplos

```bash
# Gráfico por defecto (2 años)
fibo SAN.MC

# Desde una fecha
fibo SAN.MC 2024-01-01

# Rango de fechas
fibo SAN.MC 2024-01-01 2025-06-01

# Bitcoin
fibo BTC-USD

# Apple
fibo AAPL 2023-01-01

# S&P 500 ETF
fibo SPY
```

## Indicadores incluidos

- **Niveles Fibonacci** (retroceso desde mínimos a máximos del período)
- **SMA 90** (media móvil 90 días)
- **SMA 200** (media móvil 200 días)
- **Bollinger Bands** (20 períodos)
- **MACD** (12, 26, 9)
- **RSI** (14 períodos)
- **Volumen**

## Tickers comunes

| Activo | Ticker |
|--------|--------|
| Banco Santander | SAN.MC |
| Iberdrola | IBE.MC |
| Telefónica | TEF.MC |
| Inditex | ITX.MC |
| Bitcoin | BTC-USD |
| Ethereum | ETH-USD |
| S&P 500 ETF | SPY |
| Nasdaq ETF | QQQ |
| Apple | AAPL |
| Tesla | TSLA |
| NVIDIA | NVDA |

## Salida

El gráfico se guarda en `/tmp/<TICKER>_chart.png`

Para enviarlo por Telegram:
```python
# Copiar a workspace
cp /tmp/<TICKER>_chart.png /home/gerion/.openclaw/workspace/<TICKER>_chart.png

# Enviar
message(action="send", channel="telegram", target="257331761", media="/home/gerion/.openclaw/workspace/<TICKER>_chart.png")
```

## Notas

- El script de gráficos está en: `/home/gerion/.openclaw/workspace/fibo_chart.py`
- Requiere `yfinance`, `matplotlib`, `pandas`, `numpy`
- El PATH debe incluir `~/.local/bin` o usar la ruta completa
