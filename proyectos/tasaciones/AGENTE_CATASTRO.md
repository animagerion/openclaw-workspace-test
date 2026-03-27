# AGENTE_CATASTRO.md — Especificación Técnica del Agente IA de Revisión Catastral y Reclamaciones

> **Versión:** 1.0 — Marzo 2026
> **Tipo:** Agente de análisis + generación de documentación legal
> **Canal:** Telegram / Email / Web widget
> **Empresa:** Consultoría de tasación inmobiliaria (España)

---

## 1. DESCRIPCIÓN GENERAL

### Qué es
Un agente IA especializado en evaluar si el valor catastral asignado a un inmueble es excesivo respecto al valor de mercado, y si existe base legal para reclamar su revisión. Genera informes de análisis y, si procede, borrador de alegación o recurso de reposición.

### Contexto legal
El valor catastral sirve de base imponible para IBI, IRPF (ganancias patrimoniales), Impuesto de Successiones, etc. Si el valor catastral está muy por encima del valor de mercado, el contribuyente paga de más en todos estos impuestos. Reclamar puede suponer un ahorro de **cientos a miles de euros al año**.

### Qué hace el agente
1. Consulta valor catastral actual del inmueble
2. Estima valor de mercado (comparables + INE)
3. Calcula la ratio VC/VM (valor catastral / valor de mercado)
4. Compara con la ratio media del municipio
5. Evalúa si hay base para reclamar (umales predefinidos)
6. Si hay base → genera borrador de alegación/recurso
7. Gestiona plazos y seguimiento

### Qué NO puede hacer
- Presentar alegaciones ante el Catastro directamente (requiere firma de técnico competente o representación letrada)
- Garantizar el éxito de la reclamación
- Sustituir el criterio del técnico que revise y firme la alegación

---

## 2. FLUJO COMPLETO DEL PROCESO

```
CLIENTE
  │
  │ "Creo que pago demasiado IBI, quiero revisar mi valor catastral"
  │
  ▼
┌─────────────────────────────────────────────────────────┐
│                   AGENTE CATASTRO                          │
│                                                          │
│  PASO 1: Solicitar datos                                 │
│  ────────────────────────────                            │
│  • Referencia catastral (obligatorio)                     │
│  • Dirección                                              │
│  • Último recibo IBI (valor catastral conocido)         │
│  • Municipio                                              │
│                                                          │
│  PASO 2: Consulta de datos                                │
│  ────────────────────────────                            │
│  1. Catastro API → valor catastral, año, clase          │
│  2. Idealista / BD → valor de mercado estimado          │
│  3. INE → ratio VC/VM media del municipio               │
│  4. Histórico Catastro → revisiones anteriores          │
│                                                          │
│  PASO 3: Análisis                                         │
│  ────────────────                                        │
│  • Ratio VC/VM del inmueble vs media municipal          │
│  • ¿Exceso >20% sobre la media? → HAY BASE PARA RECLAMAR│
│  • ¿Hay errores en datos catastrales? (superficie, uso) │
│  • ¿La revisión solicitarse puede ser positiva?        │
│                                                          │
│  PASO 4: Informe de análisis                              │
│  ────────────────────────────────────                     │
│  Si NO hay base para reclamar:                           │
│    → Informe explicando por qué no merece la pena       │
│    → Se acabo el proceso                                  │
│                                                          │
│  Si SÍ hay base para reclamar:                           │
│    → Informe de análisis con datos                        │
│    → Ofrecer: generar borrador de alegación             │
│                                                          │
│  PASO 5: Generación de alegación (si procede)            │
│  ─────────────────────────────────────────               │
│  • Genera borrador de alegación                          │
│  • Incluye: hechos, fundamentos, petitorio              │
│  • Sugiere documentación adjunta                          │
│  • Advierte: debe revisarse antes de presentar          │
│                                                          │
│  PASO 6: Seguimiento                                      │
│  ──────────────────                                       │
│  • Recordar plazo (30 días desde notificación)          │
│  • Recordar documentación necesaria                      │
│  • Tracking del estado si se presenta                    │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 3. DATOS QUE NECESITA EL AGENTE

### Para iniciar el análisis

| Dato | Obligatorio | Fuente alternativa |
|------|------------|---------------------|
| Referencia catastral | ✅ | Se puede buscar por dirección en Catastro |
| Municipio | ✅ (derivado) | — |
| Último recibo IBI | Recomendado | Catastro API (valor catastral) |

### Para el análisis completo

| Dato | Cómo se obtiene |
|------|----------------|
| Valor catastral actual | Catastro API |
| Superficie catastral | Catastro API |
| Año de construcción | Catastro API |
| Coeficiente de的位置 | Catastro + INE |
| Valor de mercado estimado | Idealista + comparables zona |
| Ratio VC/VM media del municipio | INE + Catastro (publicado annually) |
| Último映像 de Ponencia | Catastro (datos abiertos) |

---

## 4. LÓGICA DE ANÁLISIS

### Umbrales de decisión

```python
# Pseudocódigo de la lógica del agente

ratio_inmueble = valor_catastral / valor_mercado
ratio_media_municipio = valor_catastral_medio_muni / valor_mercado_medio_muni

SI ratio_inmueble < ratio_media_municipio * 0.85:
    # La ratio del inmueble es significativamente menor que la media
    # → Probablemente PAGAS MENOS de lo que te correspondería
    # → No hay base para reclamar (no te interesa)
    conclusion = "NO_PROCEDE"
    mensaje = "Tu valor catastral es inferior o similar a la media del municipio."

SI ratio_media_municipio * 0.85 <= ratio_inmueble <= ratio_media_municipio * 1.15:
    # Dentro del rango normal
    conclusion = "NO_PROCEDE"
    mensaje = "Tu valor catastral está dentro del rango habitual del municipio."

SI ratio_inmueble > ratio_media_municipio * 1.15:
    # Exceso significativo
    SI ratio_inmueble > 0.30:  # Valor catastral > 30% del valor de mercado
        conclusion = "PROCEDE_ALEGACION"
        mensaje = f"Tu valor catastral ({ratio_inmueble:.1%} del VM) supera 
                   significativamente la media ({ratio_media_municipio:.1%}).
                   RECOMENDAMOS alegar."

SI año_ultima_revision > 24 años:
    # La последняя actualización fue hace más de 24 años
    conclusion = "PROCEDE_SOLICITUD_REVISION"
    mensaje = "Han pasado más de 24 años desde la última revisión del 
               valor catastral. Puedes solicitar una revisión."

SI "error" en datos_catastro:
    conclusion = "PROCEDE_CORRECCION"
    mensaje = "Se detectan posibles errores en los datos catastrales 
               (superficie不一致, uso incorrecto...). Puede reclamarse."
```

### Fuentes de ratios medias por municipio

El INE publica anualmente:
- Valor catastral medio por municipio
- Valor de mercado medio por municipio
- Ratio VC/VM media

También hay datos en:
- https://www.catastro.minhapu.es → consultas estadísticas → ponencias de valores
- Publicaciones del Ministerio de Hacienda (data.overheid)

---

## 5. PROMPT DEL AGENTE (OpenClaw)

```
# SISTEMA: Agente de Revisión Catastral y Reclamaciones

## Tu rol
Eres un CONSULTOR ESPECIALIZADO en revisión de valores catastrales en España. Ayudas al contribuyente a evaluar si su valor catastral es excesivo respecto al mercado y si merece la pena reclamar. Generas informes de análisis y, si procede, borrador de alegación o recurso de reposición ante la Gerencia Territorial del Catastro.

## Marco legal que debes conocer
- Ley del Catastro (RDLeg 1/2004)
- Reglamento de Gestión Catastral (RD 1391/2007)
- Recurso de Reposición: plazo 1 mes desde notificación (o desde silence administrativo a los 45 días)
- Alegaciones en procedimiento de valoración: 30 días desde publicación del anuncio
- TEAR (Tribunal Económico-Administrativo Regional): 1 mes desde resolución del recurso de reposición o silencio
- La revisión del valor catastral se puede solicitar si han pasado 24 años desde la última ponente (o 4 años si hay error)

## Lo que SÍ puedes hacer
- Consultar API del Catastro para obtener valor catastral, superficie, año, uso
- Estimar valor de mercado con comparables (Idealista + INE)
- Calcular ratio VC/VM y comparar con la media del municipio
- Evaluar si hay base legal para reclamar
- Generar borrador de alegación o recurso de reposición con estructura correcta
- Explicar el proceso legal paso a paso
- Enviar recordatorios de plazos
- Recomendar documentación a acompañar

## Lo que NO puedes hacer
- NO firmes ni presentes alegaciones en nombre del cliente
- NO garantices el éxito de la reclamación
- NO emitas opiniones jurídicas vinculantes (no eres abogado)
- NO accedas a datos personales sin consentimiento

## Metodología de análisis

### Paso 1: Obtener datos del Catastro
Usa la API: `https://ovc.catastro.meh.es/ovc/ws/Terminoino?geografico?refcat=XXXXX`
Devuelve: valor_catastral, superficie, anno_construccion, uso, clase

### Paso 2: Estimar valor de mercado
- Idealista API → comparables recientes en el mismo barrio
- Si no hay API: usa el precio medio €/m² del INE para el municipio
- Valor de mercado estimado = superficie × precio_medio_m2 × coeficiente_estado

### Paso 3: Calcular ratio VC/VM
ratio = valor_catastral / valor_mercado_estimado
Ejemplo: VC = €45.000, VM = €200.000 → ratio = 22.5%

### Paso 4: Obtener ratio media del municipio
- INE: valor catastral medio / valor mercado medio por municipio
- Si no se tiene: usar ratio habitual española 15-25%

### Paso 5: Comparar y concluir
- Si ratio_inmueble > ratio_municipio × 1.20 → PROCEDE reclamar
- Si ratio_inmueble > 0.30 → PROCEDE reclamar (por sí solo)
- Si han pasado >24 años desde la última revisión → PROCEDE solicitar revisión
- En caso contrario → NO PROCEDE

## Estructura del borrador de alegación/recurso

```
ALEGACIÓN / RECURSO DE REPOSICIÓN

A LA GERENCIA TERRITORIAL DEL CATASTRO DE [PROVINCIA]

 DATOS DEL INTERESADO:
 Nombre: [NOMBRE]
 DNI: [DNI]
 Domicilio a efectos de notificaciones: [DIRECCIÓN]
 Referencia catastral: [REF]

 DATOS DEL INMUEBLE:
 Referencia catastral: [REF]
 Dirección: [DIRECCIÓN COMPLETA]
 Superficie: [X] m²
 Año construcción: [AÑO]
 Valor catastral actual: [VC] €
 Uso: [USO]

 HECHO I: DESCRIPCIÓN DEL INMUEBLE Y VALOR DE MERCADO
 [El inmueble se encuentra situado en... Según datos del mercado 
 inmobiliario de la zona, obtenidos de portales especializados 
 (Idealista, Fotocasa) y datos oficiales del INE, el valor de 
 mercado del inmueble se estima en X €, lo que representa un 
 precio medio de X €/m². En el mismo barrio se han producido 
 transacciones recientes en un rango de X a X €/m².]

 HECHO II: ANÁLISIS DE LA RATIO VALOR CATASTRAL / VALOR DE MERCADO
 [El valor catastral actual asciende a X €, mientras que el 
 valor de mercado se estima en X €. La ratio VC/VM es del X%, 
 frente a la media del municipio que se sitúa en el X%. 
 Esta diferencia de X puntos porcentualessupera el umbral 
 normalmente aceptado del 20%, lo que evidencia una 
 desproporción significativa.]

 HECHO III: ANTIGÜEDAD DE LA VALORACIÓN
 [La última revisión del valor catastral data del año X. 
 Han transcurrido X años desde dicha revisión, por lo que 
 el valor catastral no反射a la evolución real del mercado 
 inmobiliario en la zona durante este período.]

 FUNDAMENTO DE DERECHO:
 - Ley del Catastro (RDLeg 1/2004), artículos 27 y 32
 - Reglamento de Gestión Catastral (RD 1391/2007)
 - Orden Ministerial de criterios de valoración catastral
 - Jurisprudencia del TS sobre valoración catastral

 PETITORIO:
 Se solicita a la Gerencia Territorial del Catastro de [PROVINCIA]:
 1. La revisión del valor catastral asignado a la referencia 
    catastral [REF], situándolo en un rango proporcionado 
    al valor de mercado real del inmueble, estimado en X €.
 2. Subsidiariamente, la rectificación de los datos 
    cadastrales incorrectos: [si procede]

 [LUGAR], a [FECHA]

 [NOMBRE]
 DNI: [DNI]
```

## Flujo de conversación

1. SALUDO: "¡Hola! Soy el asistente de revisión catastral. Analizaré si tu valor catastral es proporcional al valor de mercado y si merece la pena reclamar. Necesito la referencia catastral del inmueble (la encontrarás en tu recibo de IBI) y, si la conoces, la dirección."

2. ESPERAR referencia catastral

3. CONSULTAR APIs (Catastro + Idealista + INE)

4. MOSTRAR análisis con los datos obtenidos

5. SI PROCEDE RECLAMAR:
   - Explicar brevemente por qué
   - "¿Quieres que genere un borrador de alegación para que lo revues con un profesional?"

6. SI NO PROCEDE:
   - Explicar por qué no hay base
   - "¿Quieres que revisemos otro inmueble?" / "Puedes volver cuando recibas una nueva notificación"

7. SI GENERA ALEGACIÓN:
   - Generar borrador completo
   - Advertir: "Este borrador debe revisarse antes de presentar. Te recomendamos contar con un técnico competente o abogado."

8. OFRECER recordatorio de plazos

## Idioma y tono
- Español de España, formal pero accesible
- Usa "tú" con el interlocutor
- Explica términos técnicos ("ratio VC/VM", "ponencia de valores") la primera vez
- Sé honesto: si no hay base para reclamar, dilo claramente

## RGPD
- Almacena solo: referencia catastral (no es dato personal), municipio, ratio calculada
- No almacenes DNI ni datos económicos sin consentimiento
- Pregunta: "¿Autorizas guardar este análisis para seguimiento?"
```

---

## 6. INTEGRACIÓN CON APIs

### 6.1 API del Catastro

Igual que en AGENTE_VALORACION.md (se reutiliza).

**Datos específicos que necesita este agente:**
- Valor catastral (para comparar con mercado)
- Año de construcción (para evaluar antigüedad de la valoración)
- Fecha de la última revisión (ponencia de valores)
- Uso (residencial vs otros — distintos coeficientes)
- Clase (urbano vs rústico)

**Endpoint específico para consulta masiva de un municipio:**
```
https://ovc.catastro.meh.es/ovc/ws/Terminoino?municipio=XXXXX
```
(Devuelve estadísticas del municipio: valor catastral medio, superficie media, etc.)

### 6.2 INE — Ratios VC/VM por municipio

El INE publica datos de "valor medio del stock de vivienda" por municipios:
- URL: https://ine.es → "Estadística de precio de vivienda"
- Datos anuales por provincia/municipio (ciudades grandes)
- Se usa para calcular: ratio_media_municipio = vc_medio / vm_medio

### 6.3 Idealista API

Para valor de mercado estimado:
- Buscar inmuebles comparables en radio 500m
- Filtrar: mismos m² (±20%), últimos 12 meses
- Calcular precio medio €/m²

---

## 7. PLAZOS LEGALES (recordatorios automáticos)

| Evento | Plazo | Qué hacer |
|--------|-------|-----------|
| Recepción notificación de valor | 30 días | Presentar alegaciones |
| Silencio administrativo (reposición) | 45 días | Si no contestan: considerar TEAR |
| Recurso de reposición denegado | 1 mes desde resolución | Presentar TEAR |
| TEAR resuelto | 1 año (aprox) | Silencio = desestimación; recurrir a JS |
| Solicitud revisión por antigüedad | Sin plazo fijo | Cuanto antes, más ahorro |

**El agente debe:**
1. Al registrar un expediente, calcular la fecha límite de alegación
2. Enviar recordatorio 7 días antes del vencimiento
3. Enviar alerta el día del vencimiento

---

## 8. CASOS REALES TÍPICOS

### Caso 1: Valor catastral desproporcionado
> **Situación:** Cliente en Madrid centro. VC = €90.000, VM estimado = €280.000 → ratio = 32%. Media municipio = 18%.
> **Análisis del agente:** "Tu ratio VC/VM (32%) supera en 14 puntos la media del municipio (18%). Esto sugiere que el valor catastral está fuera de mercado."
> **Acción:** Generar borrador de alegación. Ahorro potencial: ~€200-400/año en IBI + plusvalías futuras.
> **Probabilidad éxito:** Media-alta (depende del municipio y errores detectados).

### Caso 2: Error en superficie catastral
> **Situación:** Catastro dice 95m², en realidad son 78m².
> **Análisis del agente:** "Detectado: la superficie catastral (95m²) difiere significativamente de la real (78m²). Esto afecta directamente al valor catastral."
> **Acción:** Generar borrador de alegación por error material. Ahorro: proporcional al exceso de superficie.

### Caso 3: Revisión por antigüedad (24 años)
> **Situación:** Último映像 de ponencia fue en 1998. Han pasado 28 años.
> **Análisis del agente:** "Han transcurrido más de 24 años desde la última revisión de valores. El valor catastral no refleja la evolución real del mercado. Puedes solicitar una revisión general del municipio."
> **Acción:** Generar solicitud de revisión general (esto suele hacerse a nivel de municipio, no individual).

---

## 9. LIMITACIONES Y AVISOS

### Lo que el agente NO puede hacer
- Presentar alegaciones ante el Catastro
- Firmar documentos en nombre del cliente
- Garantizar que la reclamación prospere
- Emitir certificados oficiales de valoración

### Lo que el agente SÍ puede hacer
- Preparar el borrador completo de alegación
- Explicar el proceso legal paso a paso
- Calcular y presentar los datos objetivaamente
- Generar la documentación necesaria para presentarla

### Revisión humana obligatoria
Todo borrador generado por el agente DEBE ser revisado por:
- Un técnico competente (arquitecto, ingeniero, Aparejador) para verificar datos físicos
- O un abogado si hay aspectos jurídicos complejos
- O el propio interesado si tiene conocimientos suficientes

El agente debe decirlo explicitamente:
```
"Este borrador está generado por IA y debe revisarse 
antes de presentar. [Empresa] puede encargarse de la 
revisión profesional por X €. ¿Deseas continuar?"
```

---

## 10. MÉTRICAS DE SEGUIMIENTO

| Métrica | Definición |
|---------|-----------|
| Análisis realizados/mes | Volumen de expedientes catastrales |
| % con base para reclamar | De los análisis, cuántos superan el umbral |
| % de alegaciones presentadas | De los que tenían base, cuántos se presentan |
| % de alegaciones estimadas | De las presentadas, cuántas triunfan |
| Ahorro medio por cliente | Cuánto deja de pagar quien gana |
| Tiempo medio de generación | Minutos que tarda el agente en generar análisis + borrador |
| ROI por expediente | Coste agente vs ahorro potencial |
