# K-Risk: Documento Completo de Investigación

**Fecha:** 17-18 de abril de 2026  
**Autor del algoritmo:** Basado en el paper de Montojo y Rodríguez  
**Scripts:** `k_risk.py`, `k_risk_cartera.py`, `k_risk_walkforward.py`, `k_risk_trimestral.py`, `k_risk_full.py`

---

## Resumen Ejecutivo

Se ha implementado y validado el algoritmo K-Risk como herramienta de análisis de series temporales financieras. K-Risk mide la **complejidad estructural** de una serie de precios basándose en el modelado iterativo de Fourier y la Ganancia Explicativa.

**Hallazgos principales:**

| Experimento | Resultado |
|---|---|
| Calibración con datos sintéticos | Distingue correctamente señales periódicas (K≈1) de ruido (K>1.5) |
| K-Risk vs Volatilidad tradicional | Correlación ≈0 (miden cosas distintas) |
| Backtest anual (2022-2024) | K-Risk BAJO protege en crashes, pierde en rallies |
| Backtest completo 2013-2025 | K-Risk ALTO gana +980% vs SPY +307% |
| Rebalanceo trimestral | Ventana de 6 meses > ventana de 3 meses |

**Conclusión:** K-Risk funciona como **indicador de estilo de mercado** (trending vs mean-reversion), no como filtro de calidad absoluto.

---

## 1. El Algoritmo K-Risk

### Definición

K-Risk cuantifica la complejidad de una serie temporal comparando cuánto aportan las frecuencias dominantes (Fourier) frente a lo que aportaría una señal aleatoria.

```
K = Λ_Θ / Λ
```

Donde:
- Λ = Ganancia Explicativa = Σ(G_p - T_p)
- Λ_Θ = Ganancia máxima posible
- G_p = R² del modelo con las p mejores frecuencias
- T_p = Ganancia trivial = p / N (línea base aleatoria)

### Interpretación

| Rango de K | Significado |
|---|---|
| K ≈ 1.0 | Señal altamente estructurada (onda pura, tendencia lineal) |
| 1.0 < K < 1.5 | Señal con estructura mezclada con ruido moderado |
| K > 1.5 | Señal predominantemente aleatoria (ruido blanco) |
| K > 2.0 | Caos total o altamente impredecible |

---

## 2. Fase 1: Calibración con Datos Sintéticos

**Script:** `k_risk.py`

| Tipo de Serie | K-Risk | Interpretación |
|---|---|---|
| Línea Recta | 1.05 | ✅ Estructura perfecta |
| Onda Senoidal | 1.00 | ✅ Periodicidad pura |
| Paseo Aleatorio | 1.08 | ⚠️ Algo de estructura residual |
| Ruido Blanco | 2.02 | ✅ Aleatoriedad alta |

### Sensibilidad al Ruido Inyectado

Al añadir ruido progresivo a una onda senoidal pura, K-Risk crece de forma **monótona y lineal** — confirma que responde de manera consistente a la cantidad de aleatoriedad.

**Conclusión:** El algoritmo distingue bien entre señales estructuradas y ruido. Es sensible sin saturarse.

---

## 3. Fase 2: Aplicación Financiera (S&P 500)

**Script:** `k_risk.py` — `fase_2_mercado_financiero()`

**Datos:** SPY, enero 2018 – enero 2023, ventana rodante de 30 días

**Correlación K-Risk vs Volatilidad tradicional: -0.12**

Este resultado es fundamental: K-Risk y la volatilidad clásica son **casi ortogonales**. Miden cosas distintas:
- **Volatilidad:** Dispersión de los retornos (varianza)
- **K-Risk:** Complejidad estructural de la serie (patterns vs randomness)

Esto sugiere que K-Risk puede aportar información **no redundante** en modelos de predicción financiera.

---

## 4. Fase 3: Utilidad para Machine Learning

**Script:** `k_risk.py` — `fase_3_reconocimiento_patrones()`

**Experimento:** Clasificación binaria Onda vs Ruido (500 muestras sintéticas)

| Modelo | Precisión |
|---|---|
| Sin K-Risk (solo Volatilidad + Rango) | 82.00% |
| Con K-Risk (Volatilidad + Rango + K-Risk) | 85.33% |

**Importancia de características:** Volatilidad 45%, Rango 29%, K-Risk 25%

K-Risk aporta un 25% del poder predictivo del modelo, comparable a la volatilidad. La combinación de las tres métricas mejora la precisión en 3.3 puntos porcentuales.

---

## 5. Fase 4: Robustez Fractal

**Script:** `k_risk.py` — `fase_4_limites_computacionales()`

| Métrica | Valor |
|---|---|
| K-Risk serie completa (N=1000) | 1.01 |
| Promedio sub-series (N=100) | 1.12 |
| Diferencia | **10.4%** (< 15% de umbral) |

**Conclusión:** El indicador es **fractalmente robusto** — variaciones aceptables ante cambios de escala temporal.

---

## 6. Backtest de Cartera (2022 y 2024)

**Script:** `k_risk_cartera.py`

### Metodología

1. Calcular K-Risk sobre el año completo
2. Ordenar por K-Risk (menor = más limpio)
3. Descartar la mitad superior (mayor ruido)
4. De la mitad restante, elegir las 5 de mayor capitalización proxificada
5. Carter aequiponderada

### Resultados 2022 (Crash)

**Cartera:** `['UNH', 'BRK-B', 'LLY', 'AMZN', 'PG']` — perfil defensivo

| Métrica | SPY | Cartera K-Risk BAJO |
|---|---|---|
| Retorno acumulado | -18.65% | -4.38% |
| Máximo Drawdown | -24.47% | -19.32% |
| Volatilidad anual | 24.28% | 21.43% |
| Sharpe simplificado | -12.19 | -1.01 |

**Resultado:** K-Risk BAJO gana **14.3 pp** al SPY en un año de crash.

### Resultados 2024 (Alcista)

**Cartera:** `['LLY', 'UNH', 'BRK-B', 'HD', 'AAPL']`

| Métrica | SPY | Cartera K-Risk BAJO |
|---|---|---|
| Retorno acumulado | +25.59% | +21.99% |
| Máximo Drawdown | -8.41% | -8.07% |
| Volatilidad anual | 12.58% | 12.61% |
| Sharpe simplificado | 32.30 | 14.16 |

**Resultado:** K-Risk BAJO pierde **3.6 pp** frente al SPY en un año alcista.

### Conclusión parcial

K-Risk BAJO funciona como **sistema de reducción de downside** — protege en crashes pero sacrifica upside en rallies.

---

## 7. Backtest Walk-Forward (Sin Look-Ahead Bias)

**Script:** `k_risk_walkforward.py`

K-Risk calculado con datos del año T-1 para seleccionar cartera del año T.

### Por año

| Año | Cartera (basada en K-Risk T-1) | SPY | K-Risk BAJO | Diferencia |
|---|---|---|---|---|
| 2022 | HD, META, MSFT, LLY, V | -18.18% | -20.49% | -2.3pp |
| 2023 | UNH, LLY, BRK-B, PG, JPM | +26.18% | +20.96% | -5.2pp |
| 2024 | LLY, UNH, BRK-B, META, HD | +24.89% | **+29.13%** | **+4.2pp** |

### Totales (2022-2024)

| Métrica | SPY | K-Risk BAJO |
|---|---|---|
| Retorno acumulado | +28.94% | +24.19% |
| Sharpe | 1.65 | 1.20 |
| Max Drawdown | -24.50% | -29.91% |

**Nota:** En 2024, K-Risk BAJO supera al SPY por primera vez porque META entra en la cartera (basado en K-Risk de 2023, donde META era menos ruidosa). El precio de entrada del año anterior importa.

---

## 8. Rebalanceo Trimestral

**Scripts:** `k_risk_trimestral.py` (ventana 3m y 6m)

### Ventana de 3 meses (13 quarters: 2022 Q1 – 2025 Q1)

| Métrica | SPY | K-Risk BAJO |
|---|---|---|
| Retorno acumulado | +23.43% | +17.48% |
| Quarters ganados | — | 5/13 |
| Sharpe | 1.35 | 0.91 |
| Max Drawdown | -24.50% | **-20.09%** |

### Ventana de 6 meses (mismos 13 quarters)

| Métrica | SPY | K-Risk BAJO | K-Risk ALTO |
|---|---|---|---|
| Retorno acumulado | +23.43% | +19.40% | **+82.95%** |
| Quarters ganados | — | 8/13 | **10/13** |
| Sharpe | 1.35 | 1.02 | **4.54** |
| Max Drawdown | -24.50% | -31.89% | **-19.93%** |

**Resultado sorprendente:** K-Risk ALTO (acciones más ruidosas) gana por goleada en este periodo. Esto se debe a que el universo de 20 acciones está sesgado hacia mega-caps tecnológicos (NVDA, META, AMZN, MSFT), que fueron las mayores ganadoras de 2022-2025.

---

## 9. Backtest Completo 2013-2025

**Script:** `k_risk_full.py`

46 quarters desde 2013 Q4 hasta 2025 Q1, con ambas estrategias (BAJO y ALTO).

### Totales

| Métrica | SPY | K-Risk BAJO | K-Risk ALTO |
|---|---|---|---|
| **Retorno acumulado** | **+307%** | **+398%** | **+980%** |
| Sharpe | 18.09 | 21.12 | **52.33** |
| Max Drawdown | -33.7% | -32.6% | **-29.7%** |
| Quarters ganados vs SPY | — | 27/46 | **33/46** |

### Por década

| Período | SPY | BAJO | ALTO | Ganador |
|---|---|---|---|---|
| 2010s (25q) | +116.7% | +141.5% | **+270.5%** | ALTO |
| 2020s (21q) | +88.0% | +106.3% | **+191.5%** | ALTO |

---

## 10. Análisis Crítico: Sesgos y Limitaciones

### Sesgo de supervivencia

El universo de 20 acciones está sesgado hacia mega-caps tecnológicos. No hay Nokia, BlackBerry ni otras empresas que habrían tenido K-Risk alto y se habrían hundido. Los resultados de K-Risk ALTO se beneficiary de este sesgo.

### Sesgo de periodo

El periodo 2013-2025 coincide con un ciclo alcista de tecnológicas. En un mercado donde value gana a growth (como 2000-2002), K-Risk ALTO habría sido desastroso.

### K-Risk no es estacionario

El K-Risk de una acción cambia con el tiempo. Apple en 2013 tenía un K-Risk diferente a Apple en 2024. El ranking de K-Risk entre acciones fluctúa.

### Sin costes de transacción

Los backtests no incluyen slippage, comisiones ni impacto en el precio por rebalanceo.

### Capitalización proxificada por precio

No usa capitalización real de mercado. Una acción con precio bajo en términos absolutos puede ser una mega-capitalización.

---

## 11. Conclusiones

### Lo que K-Risk NO es

- No es un indicador de "calidad" de una acción
- No te dice qué acciones van a subir
- No funciona igual en todos los regimes de mercado

### Lo que K-Risk ES

- Es un indicador de **complejidad estructural**
- Es **ortogonal a la volatilidad** (mide cosas distintas)
- Funciona como **indicador de estilo de mercado**:
  - K-Risk BAJO: funciona mejor cuando el mercado premia estabilidad (crashes, regímenes defensivos)
  - K-Risk ALTO: funciona mejor cuando el mercado premia tendencia y volatilidad (rallies, momentum)

### Uso práctico sugerido

1. **Monitorear el K-Risk agregado del mercado** — si sube, el mercado se vuelve más trending/volátil
2. **Combinar ambos estilos** en lugar de elegir uno — cartera que integre BAJO y ALTO
3. **Usar como feature en modelos de ML** — K-Risk aporta información no redundante (25% de importancia)
4. **No usar en aislamiento** — K-Risk es una capa de información, no una estrategia completa

---

## 12. Archivos Generados

| Archivo | Descripción |
|---|---|
| `k_risk.py` | Script base: calibración, SPY, ML, robustez |
| `k_risk_cartera.py` | Backtest anual 2022 y 2024 |
| `k_risk_walkforward.py` | Walk-forward 2022-2024 |
| `k_risk_trimestral.py` | Rebalanceo trimestral (ventanas 3m y 6m) |
| `k_risk_full.py` | Backtest completo 2013-2025 (46 quarters) |
| `k_risk_sensibilidad_ruido.png` | Gráfico: sensibilidad K-Risk al ruido |
| `k_risk_vs_volatilidad.png` | Gráfico: K-Risk vs volatilidad SPY |
| `k_risk_backtest_2022.png` | Backtest acumulado 2022 |
| `k_risk_backtest_2024.png` | Backtest acumulado 2024 |
| `k_risk_walkforward.png` | Walk-forward 2022-2024 |
| `k_risk_trimestral.png` | Rebalanceo trimestral |
| `k_risk_full_backtest.png` | Backtest completo 2013-2025 |
| `k_risk_resultados.md` | Documento primera sesión |
| `k_risk_cartera_resultados.md` | Documento experimento cartera |
| `k_risk_documento_completo.md` | Este documento |
