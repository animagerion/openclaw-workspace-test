# AGENTE_VALORACION.md — Especificación Técnica del Agente IA de Valoración Aproximada

> **Versión:** 1.0 — Marzo 2026
> **Tipo:** Agente conversacional + инструмент de consulta APIs
> **Canal:** Telegram / Email / Web widget
> **Empresa:** Consultoría de tasación inmobiliaria (España)

---

## 1. DESCRIPCIÓN GENERAL

### Qué es
Un agente IA conversacional que atiende solicitudes de valoración aproximada de inmuebles. Recibe una dirección o referencia catastral, consulta automáticamente fuentes de datos públicas y comerciales, y devuelve un informe provisional de valoración con comparables.

### Qué NO es
- **No es un tasador homologado.** No puede emitir certificados oficiales.
- **No es un sustituto del juicio profesional.** Los datos los presenta la IA; la interpretación la hace el cliente o un tasador.
- **No garantiza precisión.** Presenta estimaciones basadas en datos disponibles.

### Objetivo de negocio
- Reducir el tiempo de respuesta de **45-90 min a 5-10 min**
- Captar leads cualificados (cliente consulta → recibe informe → decide contratar tasación completa)
- Disponibilidad 24/7 para consultas básicas

---

## 2. FLUJO DE CONVERSACIÓN COMPLETO

```
CLIENTE
  │
  │ "Hola, quiero saber cuánto vale mi piso en [dirección]"
  │
  ▼
┌─────────────────────────────────────────────────────────┐
│                 AGENTE (OpenClaw)                        │
│                                                          │
│  PASO 1: Identificar tipo de solicitud                   │
│  ───────────────────────────────────                      │
│  ¿Tiene dirección o referencia catastral?                │
│    │                                                     │
│    ├─ SÍ → Continuar                                    │
│    └─ NO → "Necesito al menos la dirección o la         │
│            referencia catastral del inmueble"            │
│                                                          │
│  PASO 2: Solicitar datos adicionales si faltan          │
│  ───────────────────────────────────────────────          │
│  • Año de construcción (o aproximado)                    │
│  • Superficie (m²) — opcional, se obtiene del Catastro  │
│  • Número de habitaciones — opcional                     │
│  • Estado del inmueble (obra nueva, buen estado, etc.)   │
│  • Motivación (venta, herencia, seguro, divorcio...)    │
│                                                          │
│  PASO 3: Consultar APIs                                  │
│  ────────────────────────                                │
│  1. Catastro → datos del inmueble                        │
│  2. Idealista → comparables en la zona                   │
│  3. INE/MITMA → índice de precio zona                    │
│  4. Histórico (propia DB) → transacciones previas        │
│                                                          │
│  PASO 4: Generar informe                                 │
│  ─────────────────────────                               │
│  • Valor estimado con rango (mínimo - máximo)           │
│  • Precio €/m² estimado                                   │
│  • Comparables encontrados (3-5)                        │
│  • Datos catastrales obtenidos                           │
│  • Indicador de confianza (alto/medio/bajo)             │
│  • Disclaimer legal                                      │
│                                                          │
│  PASO 5: Ofrecer siguiente paso                          │
│  ────────────────────────────────                        │
│  • "¿Desea que prepare un dossier completo               │
│     para una tasación oficial?"                          │
│  • "¿Quiere que analicemos si merece la pena             │
│     reclamar el valor catastral?"                        │
│                                                          │
└─────────────────────────────────────────────────────────┘
         │
         ▼
   INFORME GENERADO
   (PDF o mensaje formateado)
```

---

## 3. DATOS QUE SOLICITA AL CLIENTE

### Obligatorios (mínimo para funcionar)
| Dato | Ejemplo | Fuente alternativa si no lo da |
|------|---------|-------------------------------|
| Dirección completa | "Calle Mayor 12, 3ºB, Madrid" | Geolocalización |
| Referencia catastral | "1234567VG1234A0001" | Se puede obtener por dirección |

### Opcionales (mejoran la precisión)
| Dato | Por qué importa |
|------|-----------------|
| Año de construcción | Actualiza coeficientes correctores |
| Superficie (m²) | Más precisa que la del catastro |
| Número de habitaciones | Para comparar con Idealista |
| Planta / altura | Factor correctivo en algunos barrios |
| Estado del inmueble | Obra nueva vs necesita reforma |
| Orientación | Factor minorista |
|动机 (venta/herencia/seguro) | Adjusta el tipo de informe |

---

## 4. INTEGRACIONES CON APIs

### 4.1 API del Catastro (Sede Electrónica)

**Endpoint principal:**
```
https://ovc.catastro.meh.es/ovc/ws/Terminoino?geografico?refcat=XXXXX
https://ovc.catastro.meh.es/ovc/ws/Terminoino?geografico?municipio=XXXX&poligono=XX&parcela=XXX
```

**Datos que devuelve:**
- Referencia catastral
- Superficie (construida y útil)
- Uso (residencial, comercial)
- Clase (urbano/rústico)
- Año de construcción (rango)
- Valor catastral
- Coordenadas
- Dirección registral completa

**Ejemplo de respuesta (parsed):**
```
{
  "referencia": "1234567VG1234A0001",
  "superficie_construida": 85,
  "superficie_util": 72,
  "uso": "Vivienda",
  "clase": "Urbano",
  "anno_construccion": 1985,
  "valor_catastral": 45000,
  "latitud": 40.416775,
  "longitud": -3.703790,
  "direccion": "CL MAYOR 12 3º B MADRID"
}
```

**Coste:** Gratis (rate limit: ~1 req/segundo)

**Script de consulta (curl/bash):**
```bash
# Consulta por referencia catastral
curl -X GET "https://ovc.catastro.meh.es/ovc/ws/Terminoino?geografico?refcat=1234567VG1234A0001" \
  -H "Accept: application/json"

# Consulta por municipio + poligono + parcela
curl -X GET "https://ovc.catastro.meh.es/ovc/ws/Terminoino?geografico?municipio=07913&poligono=015&parcela=0090" \
  -H "Accept: application/json"
```

---

### 4.2 Idealista API

**Endpoint:**
```
https://api.idealista.com/api/v3.5/es/search
```

**Parámetros:**
- `location`: zona (string)
- `center`: lat,lon
- `distance`: radio en metros
- `propertyType`: flat, house
- `operation`: sale
- `maxPrice`, `minPrice`
- `size`, `rooms`

**Datos que devuelve:**
- Lista de inmuebles comparables (precio, m², habitaciones)
- Precio medio €/m² en la zona
- Fotos

**Coste:** ~€200-500/mes según volumen

**Alternativa gratuita:** Web scraping de resultados públicos (sin API key, limitado y con riesgo de bloqueo).

---

### 4.3 INE — Datos Abiertos

**URL:** https://ine.es/dyngs/INEbase/es/categoria.htm?c=Estadistica_P

**Índices útiles:**
- Índice de Precio de Vivienda (IPV) por comunidad autónoma y trimestre
- Transacciones inmobiliarias por provincia
- Serie histórico de precios por m²

**Coste:** Gratis

---

### 4.4 Propia Base de Datos (PostgreSQL/Supabase)

**Tablas:**
- `expedientes` — histórico de valoraciones realizadas
- `inmuebles` — datos conocidos de inmuebles
- `comparables` — transacciones de comparables
- `clientes` — con RGPD consent

**Consultas típicas:**
- ¿Tenemos registros previos de este inmueble?
- ¿Qué inmuebles comparables hemos tasado nearby?

---

## 5. INFORME DE VALORACIÓN — ESTRUCTURA

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📋 INFORME DE VALORACIÓN APROXIMADA
  Generado por IA — NO ES TASACIÓN OFICIAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 DATOS DEL INMUEBLE
──────────────────────────────────────────
Dirección:        Calle Mayor 12, 3ºB, Madrid
Referencia:       1234567VG1234A0001
Superficie:       85 m² construidos / 72 m² útiles
Año construcción: 1985
Uso:              Residencial
Valor catastral:  €45.000

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 VALOR ESTIMADO
──────────────────────────────────────────
Rango estimado:   €185.000 – €215.000
Punto medio:      €200.000
Precio €/m²:      ~€2.353/m² (range: €2.176–€2.529)
Confianza:        ▓▓▓▓░░ MEDIA (datos limitados)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 COMPARABLES EN LA ZONA (fuente: Idealista + BD propia)
──────────────────────────────────────────────────────────────────
#  Dirección              m²   €/m²   Precio     Distancia
1  CL PRINCIPE DE VERGARA 78   2.410   €188.000   120m
2  CL MAYOR 8 2ºA          82   2.195   €180.000   25m
3  CL ALCALA 45 4º         90   2.444   €220.000   350m
4  CL SERRANO 12 1ºB        75   2.533   €190.000   200m
5  PZ DE LA INDEPENDENCIA  88   2.045   €180.000   400m
──────────────────────────────────────────────────────────────────
Precio medio comps:   €2.325/m²
Precio medio zona INE: €2.380/m² (T4 2025, Madrid)
Diferencia con VC:    4.4x (la ratio VC/VM=22% está en rango)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 OBSERVACIONES
──────────────────────────────────────────
• El inmueble está en edificio de 1985, sin ascensor.
• La zona ha subido un 3.2% en el último año (INE).
• La ratio valor catastral / valor mercado (22%) está 
  dentro de la banda habitual (15-25%) para este municipio.
• No se han detectado reformas significativas en los 
  últimos 5 años según histórico.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  AVISO LEGAL IMPORTANTE
──────────────────────────────────────────
Este informe es una VALORACIÓN APROXIMADA generada 
por inteligencia artificial. NO tiene validez legal 
para operaciones financieras, bancarias o judiciales.

Para una TASACIÓN OFICIAL HOMOLOGADA (necesaria para 
hipotecas, litigios, etc.), contacte con un tasador 
homologado por el Banco de España.

Los datos proceden de fuentes públicas (Catastro, INE, 
portales inmobiliarios) y pueden contener inexactitudes. 
EG Consultoría declina responsabilidad por decisiones 
tomadas en base a este informe sin verificación profesional.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

¿HACEMOS UNA TASACIÓN COMPLETA?
Si necesita un informe oficial, podemos prepararle 
un dossier completo para que uno de nuestros tasadores 
homologados lo revise y firme.

¿QUIERE ANALIZAR SU VALOR CATASTRAL?
Si el valor catastral le parece alto, podemos evaluar 
si hay base para reclamar una revisión.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 6. PROMPT DEL AGENTE (OpenClaw)

```
# SISTEMA: Agente de Valoración Aproximada de Inmuebles

## Tu rol
Eres un CONSULTOR ESPECIALIZADO en valoración inmobiliaria española. Tu función es接待ar solicitudes de valoración aproximada, consultar fuentes de datos públicas, y devolver un informe provisional de valor estimado.

## Lo que SÍ puedes hacer
- Consultar la API del Catastro (ovc.catastro.meh.es) con la referencia catastral o dirección
- Buscar comparables en Idealista y otras fuentes públicas
- Consultar datos del INE sobre precios de vivienda
- Calcular rangos de valor basado en metodología de mercado (comparativos)
- Generar informes estructurados con disclaimer legal
- Responder dudas generales sobre el proceso de tasación

## Lo que NO puedes hacer (¡ IMPORTANTE!)
- NO eres un tasador homologado — no puedes firmar tasaciones oficiales
- NO emitas este informe como "tasación oficial" ni "certificado"
- NO garantices la precisión del valor — es una aproximación
- NO accedas a datos personales sin consentimiento explícito
- NO tomes decisiones legales en nombre del cliente

## Metodología de valoración
1. Obtén datos del Catastro (superficie, año, valor catastral, coordenadas)
2. Obtén comparables de Idealista (mismo barrio, últimos 6 meses, ±20% m²)
3. Calcula precio medio €/m² de comparables
4. Aplica corrección por antigüedad (coeficiente reductor si >30 años: -5% cada 10 años)
5. Aplica corrección por estado (si el cliente indica que necesita reforma: -10%)
6. Genera rango: punto medio ±10%
7. Calcula ratio VC/VM y compárala con media del municipio

## Sources de datos que tienes disponibles
- API Catastro: ovc.catastro.meh.es/ovc/ws/
- INE datos abiertos: ine.es
- Idealista API (API key configurada)
- Base de datos propia de expedientes

## Flujo de conversación
1. SALUDO: "¡Hola! Soy el asistente de valoración de [Empresa]. Puedo hacerte una valoración aproximada de cualquier inmueble en España. Solo necesito la dirección o la referencia catastral."
2. ESPERAR dirección
3. Si falta algún dato opcional, preguntar: "¿Sabes la superficie aproximada o el año de construcción?"
4. CONSULTAR APIs en paralelo
5. GENERAR informe
6. OFRECER siguientes pasos (tasación completa, revisión catastral)
7. DESPEDIDA con disclaimer

## Formato de respuesta
- Usa markdown estructurado
- Incluye siempre el AVISO LEGAL al final
- Señala claramente el nivel de confianza (ALTO/MEDIO/BAJO)
- Los datos del Catastro preséntalos siempre verbatim, indicando "datos oficiales"

## Idioma
Responde SIEMPRE en español de España. Usa un tono profesional pero cercano. "Madrid" no "Madriz", "piso" no "departamento".

## RGPD
- No guardes datos personales sin consentimiento explícito
- Después de generar el informe, pregunta: "¿Autorizas a guardar tus datos parafuturos informes?"
- Si dice que no, borra la conversación o marca como ephemeral

## Si el usuario pide algo fuera de tu alcance
"Entiendo lo que necesitas, pero para [eso] necesitas un tasador homologado / un abogado / un procedimiento formal. Te puedo derivar a nuestro equipo o explicarte cómo funciona el proceso."
```

---

## 7. CÓMO SE COMUNICA CON OTRAS HERRAMIENTAS

### Exportar a Valtec / OpenTas
Cuando el cliente solicita una tasación completa, el agente:
1. Genera un PDF del informe provisional
2. Lo guarda en `/expedientes/YYYY-MM/REF_provisional.pdf`
3. Crea una tarea en Notion/Trello: "Nueva solicitud tasación — [dirección]"
4. Envía notificación interna al equipo

### Notificaciones internas (OpenClaw → Slack/Email)
```json
{
  "tipo": "nueva_solicitud",
  "direccion": "CL MAYOR 12 3ºB MADRID",
  "ref_catastral": "1234567VG1234A0001",
  "valor_estimado": "€200.000",
  "confianza": "MEDIA",
  "siguiente_accion": "tasacion_oficial"
}
```

---

## 8. MEDICIÓN Y METRICAS

| Métrica | Cómo se mide |
|---------|-------------|
| Tiempo de respuesta | Timestamp entrada → timestamp informe generado |
| Conversión a tasación completa | % clientes que tras el informe piden tasación oficial |
| Satisfacción del cliente | Encuesta simple 1-5 stars (automática tras informe) |
| Precisión vs valor real | Comparar estimación con precio final de transacción (cuando se dispone) |
| Volumen mensual | Número de informes generados |

---

## 9. ESCALABILIDAD

- **Mismo agente, múltiples canales:** El agente puede atender Telegram, email, y web widget simultáneamente
- **Escalado horizontal:** Si el volumen crece, se crean instancias adicionales del agente para不同的 tipos de inmueble (residencial vs comercial vs rústico)
- **Mejora continua:** Cada expediente generado se almacena; el agente aprende de sus errores cuando se le corrige
