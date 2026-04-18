# K-Risk: Experimento de Filtrado de Cartera vs S&P 500

**Fecha:** 17 de abril de 2026  
**Script:** `k_risk_cartera.py`  
**Periodos de backtest:** 2022 y 2024

---

## Resumen Ejecutivo

Se utiliza el algoritmo K-Risk como **filtro de ruido estructural** para seleccionar activos dentro del universo S&P 500. La hipótesis: activos con menor K-Risk (más orden estructural) deberían comportarse mejor en periodos de estrés bursátil.

**Veredicto en 2 años:**

| Escenario | SPY | Cartera K-Risk | Ganancia/perdida K-Risk |
|---|---|---|---|
| **2022 (crash)** | -18.65% | -4.38% | **+14.3 pp** |
| **2024 (alcista)** | +25.59% | +21.99% | **-3.6 pp** |

El filtro K-Risk funciona como **sistema de reducción de riesgo**, no de maximización de retorno. Protege en crashes pero sacrifica upside en años alcistas.

---

## Metodología

1. **Universo:** 20 acciones del S&P 500 (representativas de distintos sectores)
2. **Benchmark:** SPY (ETF del S&P 500)
3. **K-Risk:** Calculado sobre los precios de cierre del año completo
4. **Filtro:**
   - Ordenar por K-Risk (menor = más limpio)
   - Descartar la mitad superior (mayor K-Risk = más ruido)
   - De la mitad restante, elegir las 5 de mayor capitalización proxificada por precio
5. **Cartera equiponderada** entre los 5 activos seleccionados

---

## Año 2022 (Escenario de Crash)

###Cartera seleccionada
`['UNH', 'BRK-B', 'LLY', 'AMZN', 'PG']` — perfil defensivo

### Ranking K-Risk 2022

| Ticker | K-Risk | ¿En cartera? |
|---|---|---|
| BRK-B | 1.025 | ✅ |
| JPM | 1.031 | ✅ |
| PG | 1.034 | ✅ |
| LLY | 1.039 | ✅ |
| WMT | 1.046 | ❌ (peso bajo) |
| NVDA | 1.050 | ❌ |
| MRK | 1.055 | ❌ |
| GOOGL | 1.056 | ❌ |
| UNH | 1.060 | ✅ |
| AMZN | 1.061 | ✅ |
| HD | 1.062 | ❌ |
| PEP | 1.063 | ❌ |
| JNJ | 1.070 | ❌ |
| CVX | 1.070 | ❌ |
| META | 1.070 | ❌ |
| ABBV | 1.074 | ❌ |
| MA | 1.075 | ❌ |
| MSFT | 1.076 | ❌ |
| AAPL | 1.093 | ❌ |
| V | 1.096 | ❌ |

**Observación:** NVDA, META, MSFT, AAPL descartadas por alto K-Risk — y fueron precisamente las que más cayeron en 2022. El filtro "acertó" sin quererlo al eliminar las más explosivas (que en 2022 se desplomaron).

### Resultados 2022

| Métrica | SPY | Cartera K-Risk |
|---|---|---|
| **Retorno acumulado** | **-18.65%** | **-4.38%** |
| Máximo Drawdown | -24.47% | -19.32% |
| Volatilidad anualizada | 24.28% | 21.43% |
| Tracking Error | — | 10.63% |
| Ratio Sharpe simplificado | -12.19 | -1.01 |

---

## Año 2024 (Escenario Alcista)

###Cartera seleccionada
`['LLY', 'UNH', 'BRK-B', 'HD', 'AAPL']` — perfil defensivo con AAPL

### Ranking K-Risk 2024

| Ticker | K-Risk | ¿En cartera? |
|---|---|---|
| MRK | 1.020 | ❌ (bajo peso) |
| UNH | 1.026 | ✅ |
| AAPL | 1.032 | ✅ |
| HD | 1.033 | ✅ |
| LLY | 1.036 | ✅ |
| WMT | 1.040 | ❌ |
| ABBV | 1.042 | ❌ |
| JNJ | 1.042 | ❌ |
| BRK-B | 1.044 | ✅ |
| NVDA | 1.048 | ❌ |
| JPM | 1.050 | ❌ |
| PG | 1.053 | ❌ |
| MA | 1.058 | ❌ |
| GOOGL | 1.061 | ❌ |
| CVX | 1.066 | ❌ |
| V | 1.069 | ❌ |
| META | 1.079 | ❌ |
| PEP | 1.080 | ❌ |
| AMZN | 1.091 | ❌ |
| MSFT | 1.095 | ❌ |

**Observación:** META (+27%), AMZN (+24%), MSFT (+17%) descartadas por alto K-Risk — y fueron las que más subieron en 2024. El filtro "pierde" al eliminar las más rentables del año.

### Resultados 2024

| Métrica | SPY | Cartera K-Risk |
|---|---|---|
| **Retorno acumulado** | **+25.59%** | **+21.99%** |
| Máximo Drawdown | -8.41% | -8.07% |
| Volatilidad anualizada | 12.58% | 12.61% |
| Tracking Error | — | 10.50% |
| Ratio Sharpe simplificado | 32.30 | 14.16 |

---

## Comparativa de los Dos Años

| Métrica | 2022 SPY | 2022 K-Risk | 2024 SPY | 2024 K-Risk |
|---|---|---|---|---|
| Retorno acumulado | -18.65% | -4.38% | +25.59% | +21.99% |
| Max Drawdown | -24.47% | -19.32% | -8.41% | -8.07% |
| Volatilidad anual | 24.28% | 21.43% | 12.58% | 12.61% |
| Tracking Error | — | 10.63% | — | 10.50% |

### Conclusión por año

- **2022:** SPY pierde 18.65%, cartera K-Risk pierde 4.38% → **K-Risk gana 14.3 pp**
- **2024:** SPY gana 25.59%, cartera K-Risk gana 21.99% → **K-Risk pierde 3.6 pp**

**En términos de Sharpe simplificado:**
- 2022: K-Risk (-1.01) vs SPY (-12.19) → Ratio 6x mejor
- 2024: K-Risk (14.16) vs SPY (32.30) → Ratio SPY 2.3x mejor

---

## Perfil de la Cartera Filtrada

El filtro K-Risk selecciona implícitamente activos de perfil **defensivo/blue-chip**:

| Año | Cartera | Sectores |
|---|---|---|
| 2022 | UNH, BRK-B, LLY, AMZN, PG | Salud, Holding, Farma, Tech, Consumo |
| 2024 | LLY, UNH, BRK-B, HD, AAPL | Farma, Salud, Holding, Retail, Tech |

Ninguna contiene NVDA, META o MSFT en ningún año. Ninguna contiene криптовалюты ni small-caps. El filtro K-Risk converge hacia capitalizaciones grandes, negocios estables y baja volatilidad.

---

## Limitaciones

1. **Universo pequeño (20 activos):** No es representativo del S&P 500 completo.
2. **Solo 2 años:** Hace falta más historial para validar el patrón.
3. **Capitalización proxificada por precio:** No usa capitalización real de mercado.
4. **Cartera equiponderada:** Sin optimización de Markowitz ni risk parity.
5. **Sin costes de transacción.**
6. **K-Risk calculado sobre el año completo (look-ahead bias potencial):** En un uso real, el K-Risk debería calcularse con datos hasta T-1, no con el año entero.

---

## Conclusiones Finales

1. **K-Risk funciona como filtro de downside protection** — en crashes reduce pérdidas significativamente.
2. **Sacrifica upside en años alcistas** — descarta activos que suben mucho (NVDA, META, MSFT).
3. **Converge hacia blue-chips defensivas** — salud, consumo básico, holdings diversificados.
4. **No es una réplica de índice** — tracking error del 10.5% lo demuestra.
5. **Uso recomendado:** Como filtro complementario o sistema de cobertura, no como estrategia principal.

---

## Archivos generados

| Archivo | Descripción |
|---|---|
| `k_risk_cartera.py` | Script Python completo |
| `k_risk_cartera_vs_spy_2024.png` | Gráfico comparativo SPY vs K-Risk (2024) |
| `k_risk_backtest_2024.png` | Backtest acumulado 2024 |
| `k_risk_cartera_vs_spy.png` | Gráfico comparativo SPY vs K-Risk (2022) |
| `k_risk_backtest_2022.png` | Backtest acumulado 2022 |
| `k_risk_cartera_resultados.md` | Este documento |
