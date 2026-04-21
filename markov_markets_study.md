# Procesos de Markov y Detección de Estados de Mercado
## Un estudio técnico-educativo

---

## 1. QUÉ ES UN PROCESO DE MARKOV

### 1.1 Origen

Andrei Markov (1856-1922), matemático ruso, desarrolló estos procesos entre 1906-1913. Los creó para analizar vocales en poesía Pushkin — demostrando que no eran independientes entre sí como se creía.

### 1.2 La idea central

Un proceso de Markov tiene una propiedad fundamental:

> **"El futuro depende del presente, no del pasado completo."**

Esto se llama la **propiedad de Markov** o propiedad de "memoria corta".

Formalmente:
```
P(X_t+1 = j | X_t = i, X_t-1 = i_t-1, ..., X_0 = i_0) = P(X_t+1 = j | X_t = i)
```

Es decir: para predecir el siguiente estado, solo necesitas saber el estado actual — no hace falta saber toda la historia.

### 1.3 Cadena de Markov simple

Una cadena de Markov es una secuencia de estados donde las transiciones entre ellos tienen probabilidades fijas.

**Ejemplo del tiempo:**

| Estado actual → | Soleado | Nublado | Lluvioso |
|---|---|---|---|
| Soleado | 0.7 | 0.2 | 0.1 |
| Nublado | 0.4 | 0.3 | 0.3 |
| Lluvioso | 0.3 | 0.4 | 0.3 |

Esto significa: si hoy está soleado, hay 70% de probabilidad de que mañana también sea soleado, 20% de que esté nublado, y 10% de lluvia.

**Observación clave:** La matriz de transiciones es constante en el tiempo. No cambia según el día del año.

### 1.4 Ejemplo numérico

Supongamos que hoy está soleado. ¿Qué tiempo tendremos dentro de 3 días?

```
Día 1: Soleado (100%)
Día 2: [0.7, 0.2, 0.1] = Soleado 70%, Nublado 20%, Lluvia 10%
Día 3: Multiplicamos [0.7, 0.2, 0.1] × matriz de transición
```

Con el tiempo, el sistema converge a una **distribución estacionaria** — sin importar el estado inicial, a largo plazo el sistema termina en probabilidades fijas (aproximadamente 53% sol, 26% nubes, 21% lluvia en este ejemplo).

---

## 2. MODELOS OCULTOS DE MARKOV (HMM)

### 2.1 El problema

En una cadena de Markov normal, los estados SON observables. Pero en la realidad, muchos estados relevantes SON INVISIBLES.

**Ejemplos reales:**
- En medicina: el estado de salud de un paciente no se observa directamente, solo los síntomas
- En speech recognition: no observas las "palabras" del lenguaje, solo las ondas de sonido
- En mercados: no observas directamente si el mercado está en modo "acumulación" o "distribución", solo los precios

### 2.2 Estructura de un HMM

```
ESTADOS OCULTOS (lo que NO vemos)     OBSERVACIONES (lo que sí vemos)
┌─────────────────┐                   ┌─────────────────┐
│ Acumulación     │ ──────────────→  │ Precios subiendo │
│ (smart money    │   Probabilidades │ con volumen bajo │
│  comprando)     │   de transición  │                  │
└────────┬────────┘                   └─────────────────┘
         │
┌────────▼────────┐                   ┌─────────────────┐
│ Distribución    │ ──────────────→  │ Precios bajando │
│ (smart money   │                  │ con volumen alto │
│  vendiendo)    │                  │                  │
└────────┬────────┘                   └─────────────────┘
         │
┌────────▼────────┐                   ┌─────────────────┐
│ Capitulación    │ ──────────────→  │ Caída brusca    │
│ (pánico total)  │                  │ volumen extremo  │
└─────────────────┘                   └─────────────────┘
```

Un HMM intenta responder: **"Dadas las observaciones (precios) que vi, ¿cuál era el estado oculto más probable en cada momento?"**

### 2.3 Tres problemas fundamentales de HMM

**Problema 1: Evaluación**
Dado un HMM y una secuencia de observaciones → ¿cuál es la probabilidad de esa secuencia? Útil para validar si un modelo tiene sentido.

**Problema 2: Decodificación**
Dada una secuencia de observaciones → ¿cuál fue la secuencia más probable de estados ocultos? **Este es el usado en trading.**

**Problema 3: Aprendizaje**
Dadas las observaciones → ¿cuáles son las matrices de transición y emisión que mejor explican los datos? Se usa el algoritmo de **Baum-Welch** (desarrollado por Leonard Baum de Renaissance Technologies).

---

## 3. APLICACIÓN A MERCADOS FINANCIEROS

### 3.1 La intuición

Los mercados tienen estados que no vemos directamente:

| Estado oculto | Características observables |
|---|---|
| **Acumulación** | Precios estables, volumen bajo, baja volatilidad. Smart money está entrando silenciosamente. |
| **Mark-up** | Precios subiendo con volumen moderado, tendencia alcista gradual. |
| **Distribución** | Precios subiendo pero con volumen creciente y divergencias. Smart money está saliendo. |
| **Mark-down** | Precios cayendo con volumen, tendencia bajista. |
| **Capitulación** | Caída vertical extrema, volumen de pánico,老先生 inversores venden. |
| **Rango lateral** | Sin tendencia clara, precios oscilando en rangos. |

### 3.2 Cómo funciona en la práctica

**Paso 1: Definir los estados**
El cuant decide cuántos estados quiere modelar (típicamente 2-6 para mercados):

- 2 estados: Bull / Bear
- 3 estados: Alta vol / Baja vol / Transición
- 4 estados: Accumulation / Up-trend / Distribution / Down-trend
- Más estados son posibles pero más difícil de entrenar

**Paso 2: Definir las observaciones**
¿Qué "vemos"? Las observaciones pueden ser:
- Retornos diarios
- Volatilidad realised (desviación estándar móvil)
- Ratios de volumen
- spreads entre instrumentos
- yields

**Paso 3: Entrenar con Baum-Welch**
El algoritmo toma datos históricos y encuentra:
- Las **probabilidades de transición** entre estados
- Las **distribuciones de emisión** (qué observaciones corresponden a cada estado)

**Paso 4: Decodificar (Viterbi algorithm)**
Para cada día, calcular cuál era el estado oculto más probable dado el precio/volatilidad observado.

**Paso 5: Tradear**
- Si el estado cambia de "acumulación" a "mark-up" → señal de compra
- Si cambia a "distribución" → cerrar posiciones largas
- Si estamos en "capitulación" → oportunidad de compra (pánico suele ser corto)

### 3.3 Ejemplo simplificado con números

Supongamos que definimos 2 estados: BULL (crecimiento) y BEAR (declive).

**Observables:** retornos diarios del mercado.

**Matriz de transición aprendida (hipotética):**
```
          BULL    BEAR
BULL →   [ 0.85   0.15 ]   # Si es bull, 85% probabilidad de seguir bull
BEAR →   [ 0.20   0.80 ]   # Si es bear, 80% probabilidad de seguir bear
```

**Matriz de emisiones (hipotética):**
```
          Ret>1%  Ret 0-1%  Ret -1-0%  Ret<-1%
BULL →   [ 0.30   0.40     0.25       0.05 ]  # Bull produce más retornos positivos
BEAR →   [ 0.05   0.25     0.40       0.30 ]  # Bear produce más retornos negativos
```

**Decodificación:**
Día 1: Ret = +1.5%
Día 2: Ret = -0.3%
Día 3: Ret = -2.1%
Día 4: Ret = +0.8%

Usando Viterbi: El algoritmo calcula la probabilidad de cada estado para cada día. En este ejemplo, probablemente detectaría una transición de BULL a BEAR alrededor del día 3.

### 3.4 Limitaciones

1. **El número de estados es arbitrario** — nadie sabe cuántos "modos" reales tiene el mercado
2. **Los estados pueden cambiar** — lo que hoy es "bull" puede no ser el mismo "bull" que hace 10 años
3. **No predice, solo detecta** — un HMM te dice en qué estado ESTÁS, no a cuál irás
4. **Sobreajuste** — con muchos estados y datos limitados, es fácil ajustar el modelo al ruido histórico
5. **Asume estaciones estabilidad** — la matriz de transición se asume constante, pero en crisis cambia radicalmente

---

## 4. POR QUÉ SIMONS LO USÓ (Y POR QUÉ FUNCIONÓ)

### 4.1 La conexión con NSA

Simons trabajó descifrando códigos soviéticos. En NSA:
- Las comunicaciones tienen patrones ocultos (estados)
- Solo observas la señal encriptada (observaciones)
- HMMs eran la herramienta estándar para inferir estados secretos de mensajes

La transferencia de dominio fue natural: el "ruido" del mercado es como una señal encriptada, y los estados ocultos del mercado son como los estados del mensaje original.

### 4.2 Por qué la ventaja competitiva

En los años 80-90:
- Pocos cuant firms usaban HMMs
- Menos aún tenían datos suficientes para entrenarlos bien
- Nadie combinaba HMMs con datos exóticos (precios de supermercados, datos meteorológicos)
- La velocidad de computación era cara — ahora es barata

Simon tenía:
- mathematicians que entendían HMMs (Baum Welch)
- Datos que nadie más tenía
- Velocidad de ejecución que nadie más tenía
- Cultura de "1000 pequeñas señales" en vez de "1 gran modelo"

### 4.3 La lección práctica

Un HMM bien entrenado puede detectar cambios de régimen ANTES de que sean obvios.

Ejemplo:
- Si el mercado ha estado en modo "baja volatilidad + tendencia alcista" durante semanas, y de repente los retornos empiezan a ser más erráticos...
- ...el HMM puede detectar que las probabilidades de transición están cambiando
- Esto da una señal temprana de que un régimen está terminando

---

## 5. IMPLEMENTACIÓN BÁSICA EN PYTHON

```python
# Ejemplo conceptual usando hmmlearn
from hmmlearn import hmm
import numpy as np

# Observables: retornos diarios (simplificado)
X = np.loadtxt('daily_returns.csv')  # Shape: (n_samples, 1)

# Crear HMM con 3 estados ocultos
model = hmm.GaussianHMM(n_components=3, covariance_type='full', n_iter=1000)

# Entrenar con datos históricos
model.fit(X)

# Predecir estados para datos futuros
hidden_states = model.predict(X)

# Ver probabilidades de transición
print("Matriz de transición:")
print(model.transmat_)

# Ver medias de cada estado (rentabilidad media por estado)
print("Rentabilidad media por estado:")
for i, mean in enumerate(model.means_.flatten()):
    print(f"  Estado {i}: {mean:.4f}%")
```

---

## 6. RESUMEN

| Concepto | Descripción |
|---|---|
| **Proceso de Markov** | Sistema donde el futuro solo depende del presente, no del pasado |
| **Cadena de Markov** | Secuencia de estados con probabilidades de transición fijas |
| **HMM** | Los estados reales son ocultos; solo vemos "síntomas" (observaciones) |
| **Baum-Welch** | Algoritmo para entrenar HMMs con datos históricos |
| **Viterbi** | Algoritmo para encontrar la secuencia de estados ocultos más probable |
| **Aplicación en mercados** | Inferir regímenes de mercado (bull, bear, accum, dist) desde precios observables |
| **Ventaja de Simons** | Combinación de HMMs + datos exclusivos + velocidad + 1000 señales pequeñas |

La idea central de Simons: **los mercados tienen "personalidad" que cambia entre estados. Si puedes detectar esos estados más rápido que otros, puedes posicionarte antes del cambio.**

---

## 7. FUENTES Y LECTURAS

- Rabiner, L. (1989). "A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition" — El paper fundamental sobre HMMs
- Baum, L.E. & Petrie, T. (1966). "Statistical Inference for Probabilistic Functions of Finite State Markov Chains"
- Covered Network podcast episode on Simons (acquired.fm)
- automatedtradingstrategies.substack.com — "From Codebreaking to Market Mastery"
