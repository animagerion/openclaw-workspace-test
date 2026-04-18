# K-Risk — Memorias de Trabajo

_Estado: PAUSADO (esperando datos de proveedor externo)_
_Ultima actualización: 2026-04-18_

---

## 1. Qué es K-Risk

K-Risk es un algoritmo de análisis de series temporales financieras desarrollado a partir de un paper de **Montojo & Rodríguez**. Mide la **complejidad/distribución espectral** de una serie temporal:

- Usa FFT (Transformada de Fourier) para descomponer la serie en frecuencias
- Compara cuánto explican las frecuencias dominantes (G_p, gain) vs. lo que explicaría una serie trivial equiprobable (T_p = p/N)
- K = Λ_Θ / Λ, donde Λ = Σ(G_p - T_p) y Λ_Θ = Σ(1 - T_p)
- **K bajo** → serie predecible (mucho poder predictivo en pocas frecuencias, tipo trend/momentum)
- **K alto** → serie ruidosa/compleja (frecuencias distribuidas, difícil de predecir)
- K = 1.0 → serie random (sin señal)
- K → 0 → serie altamente predecible (dominada por ciclos少数s)

En la práctica, K-Risk funciona como **indicador de régimen**:
- Mercados en tendencia (momentum): K-Risk bajo
- Mercados en rango/aleatorios: K-Risk alto

---

## 2. Scripts creados

| Script | Descripción |
|--------|-------------|
| `k_risk.py` | Función K-Risk core + 4 fases: synthetic calibration, sensitivity, S&P 500 application, ML classification, sample size robustness |
| `k_risk_cartera.py` | Filtro de cartera: top-5 más bajo K-Risk de 20 acciones S&P 500. Tests 2022 y 2024 por separado. |
| `k_risk_trimestral.py` | Rebalanceo trimestral, ventana 3m y 6m, selección BAJO y ALTO |
| `k_risk_walkforward.py` | Walk-forward anual sin look-ahead bias (train T-1, test T), 2022-2024 |
| `k_risk_full.py` | Walk-forward completo 2013 Q4 → 2025 Q1 (46 trimestres), 20 stocks |
| `k_risk_sp500_full.py` | S&P 500 completo con composición histórica (PAUSADO — datos incompletos) |

---

## 3. Documentos generados

| Documento | Contenido |
|----------|----------|
| `k_risk_resultados.md` | Fases 1-4 (calibración, sensibilidad, aplicación S&P, ML, robustez) |
| `k_risk_cartera_resultados.md` | Backtests 2022 y 2024 con 20 stocks |
| `k_risk_documento_completo.md` | TODOS los experimentos compilados (12 secciones, enviado a Paduel por Telegram) |

---

## 4. Resultados acumulados

### 4.1 Backtest 2022 (crash)
- **K-Risk BAJO (top-5 bajo K-Risk):** -4.38%
- **SPY:** -18.65%
- **Ventaja: +14.27pp** ✅

### 4.2 Backtest 2024 (bull)
- **K-Risk BAJO:** +21.99%
- **SPY:** +25.59%
- **Ventaja: -3.60pp** ❌

### 4.3 Rebalanceo trimestral (20 stocks, 2013 Q4 → 2025 Q1)

**Ventana 3m:**
- SPY: +23.43%
- K-Risk BAJO: +17.48% (gana 5/13 trimestres)
- K-Risk ALTO: +82.95% (gana 10/13 trimestres, Sharpe 4.54)

**Ventana 6m:**
- SPY: +23.43%
- K-Risk BAJO: +19.40% (gana 8/13 trimestres)
- K-Risk ALTO: +82.95% (gana 10/13 trimestres)

### 4.4 Walk-forward completo (46 trimestres)
- **SPY:** +307%
- **K-Risk BAJO:** +398% (27/46 wins)
- **K-Risk ALTO:** +980% (33/46 wins), Sharpe 52.33, MaxDD -29.7%

---

## 5. Interpretación clave

**CRÍTICO — Sesgo de supervivencia:**

El resultado "K-Risk ALTO gana más" en nuestro universo de 20 acciones es un **artefacto del periodo y el universo**:

1. El universo está sesgado hacia mega-caps tecnológicos (AAPL, MSFT, GOOGL, AMZN, NVDA, META = 6/20)
2. K-Risk ALTO selecciona acciones con más ruido/complejidad, que tienden a ser high-beta
3. 2013-2025 fue un periodo extraordinariamente favorable para tech/high-beta
4. **Esto NO significa que K-Risk ALTO sea mejor que BAJO en general**

K-Risk funciona como **indicador de régimen**:
- **K-Risk bajo** = entorno de momentum/tendencia (como 2022 crash — funciona bien defensivo)
- **K-Risk alto** = entorno de rango/aleatoriedad (como ciertos quarters de 2013-2025)

En un universo más amplio y diversificado, K-Risk BAJO probablemente sería neutral o mejor en promedio.

---

## 6. Problema actual: datos incompletos

### Situación:
- CSV de composición histórica: `fja05680/sp500` en GitHub
- Solo llega hasta **2019-01-11** (faltan 6+ años: COVID, 2020-2025 bull market)
- yfinance tiene ~670/1027 tickers (muchos delistados sin datos)
- El backtest `k_risk_sp500_full.py` no genera resultados porque:
  - Faltan datos de los últimos años
  - Muchos tickers delistados no tienen datos en yfinance

### Lo que necesitamos:
1. **Datos de composición trimestral del S&P 500** desde ~1996 hasta 2025 (de un proveedor externo)
2. **Precios de cierre trimestrales** de todos los componentes históricos (adj. close)
3. Formato ideal: CSV con columnas `date, ticker, adj_close` o similar

### Paduel está buscando un proveedor de datos.

---

## 7. Próximos pasos (cuando lleguen los datos)

### Prioridad 1: Backtest S&P 500 completo (50 componentes, 1996-2025)
- Script ya preparado: `k_risk_sp500_full.py`
- Solo hay que reemplazar la fuente de datos
- Validar si K-Risk BAJO o ALTO gana en un universo amplio y en varios periodos

### Prioridad 2: Test de hipótesis adicionales
1. **K-Risk como régimen vs. filtro de calidad**: ¿K-Risk bajo = defensive/quality en todos los entornos?
2. **K-Risk + mean reversion**: Combinar K-Risk bajo con señales de mean reversion
3. **K-Risk vs. factor momentum**: ¿K-Risk es redundante con momentum o aporta información independiente?
4. **K-Risk en otros activos**: Bonos, commodities, crypto — ¿K-Risk bajo predice tendencias?

### Prioridad 3: Producción
- Si los resultados se replican, integrar K-Risk en operativa real
- Parámetros a optimizar: ventana de cálculo, percentil de corte (K-Risk BAJO vs ALTO), universo, rebalanceo

---

## 8. Bugs y lecciones aprendidas

- **Córdoba (code 14)** en Catastro API da 500. Workaround: usar "CORDOBA" sin acento.
- **BRK-B, BF.B, RDS.A** son tickers con guiones/puntos que dan errores en yfinance.
- **No usar sed con patrones complejos** — corrompe archivos. Editar manualmente o reescribir.
- **Survivorship bias** es siempre un riesgo cuando se testean universos que "sobreviven". El universo de 20 acciones ya está sesgado.

---

## 9. Archivos relacionados

```
k_risk.py
k_risk_cartera.py
k_risk_trimestral.py
k_risk_walkforward.py
k_risk_full.py
k_risk_sp500_full.py         ← PAUSADO
k_risk_resultados.md
k_risk_cartera_resultados.md
k_risk_documento_completo.md ← Documento principal (enviado por Telegram)
sp500_historical.csv          ← Composición histórica (incompleta: solo hasta 2019)
```

---

## 10. Para retomar

1. Leer `k_risk_documento_completo.md` para contexto completo
2. Leer `k_risk.py` para la función K-Risk core
3. Leer `k_risk_sp500_full.py` para el script de backtest S&P 500 completo
4. Cuando lleguen los datos del proveedor, ejecutar `k_risk_sp500_full.py`
5. Analizar resultados y decidir siguiente paso
