# 🤖 Bot de Trading Simulado

Estrategia de trading algorítmico con análisis técnico para simulación.

## 📋 Requisitos

```bash
pip install yfinance pandas numpy matplotlib
```

## 🚀 Uso

### Uso básico
```bash
python3 scripts/trading_bot.py
```

### Con argumentos personalizados
```bash
# Diferente ticker
python3 scripts/trading_bot.py --ticker MSFT

# Diferente período
python3 scripts/trading_bot.py --ticker SPY --start 2022-01-01 --end 2024-12-31

# Diferente capital inicial
python3 scripts/trading_bot.py --ticker AAPL --capital 50000
```

## 📊 Estrategias Implementadas

### 1. SMA Crossover (Cruce de Medias Móviles)

**Lógica:**
- **COMPRAR** cuando la SMA corta cruza **encima** de la SMA larga (señal bullish)
- **VENDER** cuando la SMA corta cruza **debajo** de la SMA larga (señal bearish)

**Parámetros por defecto:**
- SMA corta: 20 días
- SMA larga: 50 días

**Ventajas:**
- Elimina subjetividad
- Sigue la tendencia
- Funciona bien en mercados con tendencia definida

**Desventajas:**
- Señales falsas en mercados laterales
- Retraso en entrar/salir

### 2. RSI (Relative Strength Index)

**Lógica:**
- **COMPRAR** cuando RSI sale de la zona de sobreventa (<30)
- **VENDER** cuando RSI entra en zona de sobrecompra (>70)

**Parámetros por defecto:**
- Período: 14 días
- Sobreventa: 30
- Sobrecompra: 70

**Ventajas:**
- Detecta sobrecompra/sobreventa
- Funciona bien en mercados laterales

**Desventajas:**
- Puede mantenerse en sobrecompra/sobreventa mucho tiempo
- Señales tardías

## 📈 Métricas de Rendimiento

| Métrica | Descripción |
|---------|-------------|
| Retorno Total | Porcentaje de ganancia/pérdida |
| Buy & Hold | Retorno si hubieras comprado y mantenido |
| Max Drawdown | Mayor caída desde un pico |
| Win Rate | Porcentaje de trades winners |
| Número de Trades | Total de operaciones |

## 📁 Output

- **Gráfico PNG** guardado en `/tmp/trading_{ticker}_{fecha}.png`
- **Resultados en consola** con todas las métricas

## ⚠️ LIMITACIONES Y DISCLAIMER

### IMPORTANTE: Esto es SIMULACIÓN, NO es asesoramiento financiero.

1. **Los resultados pasados NO garantizan resultados futuros**
   - Una estrategia que funcionó bien históricamente puede fallar completamente

2. **No considera:**
   - Costes de transacción (spread, comisiones)
   - Slippage (diferencia entre precio esperado y real)
   - Liquidez del mercado
   - Volumen de trading
   - Noticias y eventos del mercado
   - Impuestos

3. **Overfitting (sobreoptimización):**
   - Los parámetros están ajustados a datos históricos
   - No hay garantía de que funcionen en datos futuros

4. **No es dinero real:**
   - Las simulaciones usan precios de cierre
   - En la realidad, el precio de ejecución puede diferir
   - No hay "market impact" simulado

5. **Este bot es EDUCATIVO:**
   - Úsalo para aprender y entender estrategias
   - Para trading real, usa brokers regulados con gestión de riesgo
   - Consulta con profesionales financieros

## 🛠️ Personalización

Modifica `DEFAULT_CONFIG` en el script para cambiar:

```python
DEFAULT_CONFIG = {
    "ticker": "AAPL",        # Tu símbolo
    "start_date": "2023-01-01",
    "end_date": "2024-12-31",
    "sma_short": 20,         # Período SMA corta
    "sma_long": 50,          # Período SMA larga
    "rsi_period": 14,        # Período RSI
    "rsi_oversold": 30,      # Nivel de sobreventa
    "rsi_overbought": 70,    # Nivel de sobrecompra
    "initial_capital": 10000.0,
}
```

## 📚 Recursos

- [yfinance](https://github.com/ranaroussi/yfinance) - Descarga de datos
- [pandas](https://pandas.pydata.org/) - Análisis de datos
- [matplotlib](https://matplotlib.org/) - Visualización

---

*Creado con fines educativos. No es asesoramiento financiero.*
