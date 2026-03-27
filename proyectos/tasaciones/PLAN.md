# PLAN.md — Automatización con IA para Empresa de Tasación de Inmuebles

> **Versión:** 1.0 — Marzo 2026
> **Enfoque:** España — Empresa de tasación residencial y comercial

---

## 1. RESUMEN EJECUTIVO

Una empresa de tasación media en España recibe solicitudes de tres tipos: **(a)** valoraciones aproximadas para particulares (compraventa, herencia, divorcios), **(b)** tasaciones oficiales homologadas para банков (hipotecas), y **(c)** revisiones de valor catastral para reclamaciones. Las tres se benefician enormemente de IA, pero en grados distintos.

**Lo que se puede automatizar ahora con IA (sin cruzar la línea legal):**

| Tipo | Automatizable | Ahorro estimado | Legal |
|------|--------------|-----------------|-------|
| Valoración aproximada (no oficial) | **80%** del trabajo previo | 45-60 min por expediente | ✅ Con disclaimer obligatorio |
| Soporte al tasador (pre-visita) | **70%** del trabajo de recherche | 30-40 min por expediente | ✅ IA como herramienta del tasador |
| Tasación oficial (hipoteca) | **30%** | 15-20 min por expediente | ⚠️ Solo como apoyo; firma requiere homologado |
| Revisión catastral + alegaciones | **85%** | 60-90 min por expediente | ✅ IA para preparar documentación |

**Ahorro global estimado:** 3-5 horas/hombre por día laborable en una empresa de 5 tasadores. ROI positivo en **2-4 meses**.

---

## 2. CASOS DE USO PRIORITARIOS (priorizados por impacto/facilidad)

### 🔴 PRIORIDAD 1: Valoración aproximada (no oficial)
- **Qué es:** Informe preliminar para cliente final (no homologado, no para банк)
- **Qué hace el agente IA:**
  1. Recibe dirección o referencia catastral del cliente
  2. Consulta automáticamente Catastro → datos del inmueble
  3. Consulta Idealista/Fotocasa → precios de vivienda en la zona
  4. Consulta registros de transacciones (INE, MITMA) → índices de precio
  5. Genera un informe provisional con rango de valor estimado
- **Input cliente:** Dirección + referencia catastral (opcional) + motivo valoración
- **Output:** Informe PDF/email con valor estimado, comparables, y disclaimer legal
- **Tiempo actual (manual):** 45-90 min | **Tiempo con IA:** 5-10 min
- **Impacto:** Alto — es el servicio de mayor volumen y menor margen actual

### 🟡 PRIORIDAD 2: Soporte pre-visita al tasador
- **Qué es:** Dossier automático antes de la visita física
- **Qué hace el agente IA:**
  1. Búsqueda de antecedentes del inmueble en Catastro + Registro
  2. Comprobación de cargas y gravámenes (virtual, cuando sea posible)
  3.-localización de comparables vendidos en la zona (últimos 2 años)
  4. Extracción de fotos del entorno (Google Street View, Idealista)
  5. Histórico de precios en la zona (registro de la propiedad de二年)
  6. Preparación de checklist de datos a verificar in situ
- **Tiempo actual:** 40-60 min | **Tiempo con IA:** 5-8 min
- **Impacto:** Alto — el tasador se presenta con un dossier completo; menos visitas de vuelta

### 🟡 PRIORIDAD 3: Revisión de valores catastrales y alegaciones
- **Qué es:** Análisis automático de si hay base para reclamar + generación de alegación
- **Qué hace el agente IA:**
  1. Consulta valor catastral actual (Catastro)
  2. Consulta valor de mercado estimado (Idealista, registros)
  3. Calcula la ratio VC/VM y la compara con la media del municipio
  4. Evalúa antigüedad, coeficientes, y，恶补了一下法规...
  5. Si hay base para reclamar → genera borrador de alegación/recurso
- **Tiempo actual:** 60-120 min | **Tiempo con IA:** 10-15 min
- **Impacto:** Medio-alto — volumen menor pero alto valor para el cliente (en juego hay miles de euros)

### 🟢 PRIORIDAD 4: Integración con herramientas de tasación existentes
- **Qué es:** Conectar el agente IA con Valtec / OpenTas / Tecoh
- **Qué hace:** Exportar datos ya obtenidos directamente al formato de la herramienta
- **Tiempo actual:** 20-30 min de transcripción manual | **Tiempo con IA:** 0 (automático)
- **Impacto:** Medio — facilita adopción por parte de los tasadores

---

## 3. ARQUITECTURA DEL SISTEMA

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENTE / USUARIO                        │
│          (particular, banco, administrador)                 │
└─────────────────────┬───────────────────────────────────────┘
                      │ Telegram / WhatsApp / Web / Email
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              AGENTE IA PRINCIPAL (OpenClaw)                 │
│  • Gestiona conversación                                     │
│  • Orquestra subagentes                                      │
│  • Genera documentos PDFs                                    │
│  • Envía emails / notificaciones                             │
└──────────┬──────────────────┬───────────────────┬──────────┘
           │                  │                   │
           ▼                  ▼                   ▼
┌──────────────────┐ ┌─────────────────┐ ┌──────────────────┐
│  AGENTE VALORA.  │ │ AGENTE CATASTRO │ │ AGENTE TASADOR   │
│  (valoración     │ │ (revisiones     │ │ (soporte pre-     │
│   aproximada)    │ │  catastrales)   │ │  visita)         │
└────────┬─────────┘ └────────┬────────┘ └────────┬─────────┘
         │                    │                   │
         ▼                    ▼                   ▼
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE DATOS / APIs                     │
│                                                              │
│  🔵 Catastro (ovc.catastro.meh.es) — datos inmueble         │
│  🔵 Registro de la Propiedad — cargas, antecedentes          │
│  🔵 Idealista API — comparables, precios zona                │
│  🔵 INE/MITMA — índices precio vivienda                      │
│  🔵 Sedecatastro — cartografía, referencia catastral         │
│  🔵 Base de datos propia — histórico de expedientes           │
└─────────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                 ALMACÉN DE DOCUMENTOS                       │
│  • Informes generados (PDF)                                   │
│  • Alegaciones generadas                                      │
│  • Dossiers de tasador                                        │
│  • Históricos de conversación                                 │
└─────────────────────────────────────────────────────────────┘
```

### Flujo de datos

1. **Cliente contacta** → Agente IA identifica el tipo de solicitud
2. **Clasificación:**
   - ¿Valoración aproximada? → Agente Valoración
   - ¿Reclamación catastral? → Agente Catastro
   - ¿Tasación oficial? → Agente Tasador (soporte) → Tasador homologado firma
3. **El agente consulta APIs** → Compila datos → Genera documento
4. **Revisión humana** (mínimo para tasaciones oficiales)
5. **Entrega al cliente**

---

## 4. STACK TECNOLÓGICO

### Plataforma central: OpenClaw
| Función | Cómo se usa |
|---------|------------|
| Agente conversacional | Interfaz con el cliente (Telegram, email, web) |
| Orquestación | Dispara subagentes según tipo de solicitud |
| Acceso APIs | Ejecuta llamadas HTTP a Catastro, Idealista, etc. |
| Generación documentos | Crea PDFs con datos obtenidos |
| Base de datos | Almacena expedientes y historique |
| Programación | Tareas nocturnas, alarmas de plazos |

**Coste OpenClaw:** ~€29-99/mes según plan (ver pricing openclaw.ai)

### APIs y fuentes de datos

| Fuente | Qué ofrece | Coste | Acceso |
|--------|-----------|-------|--------|
| **Sede Electrónica Catastro** | Valor catastral, referencia, superficie, uso, clase | **Gratis** (rate limited) | `ovc.catastro.meh.es/ovc/ws/` — SOAP/REST |
| **Idealista API** | Precios por zona, comparables, fotos | ~€200-500/mes | idealista.com/api — REST API key |
| **Fotocasa API** | Alternativa a Idealista | Variable | fotocasa.es/api |
| **Registro de la Propiedad** | Cargas, gravámenes (parcial) | **Gratis** para consulta básica | `registropropiedad.es` |
| **INE** | Índices precio vivienda, transacciones | **Gratis** | ine.es — datos abiertos |
| **MITMA** | Indices precio vivienda oficial | **Gratis** | `#datos` |
| **Google Maps / Street View** | Fotos entorno, coordenadas | **Gratis** (con cuota) | Google Cloud API |

### Herramientas complementarias

| Herramienta | Uso | Coste |
|-------------|-----|-------|
| **n8n** | Orquestación de flujos automatizados (alternativa a OpenClaw para workflows específicos) | Self-hosted gratis / Cloud ~€20/mes |
| **Make.com** | Sin código — automatización de tareas repetitivas | ~€9-29/mes |
| **Zapier** | Similar a Make, más internacional | ~€19-49/mes |
| **Valtec** | Software de tasación (integración de datos) | ~€100-200/mes |
| **OpenTas** | Gestión integral de expedientes de tasación | ~€150-300/mes |
| **Tecoh** | another tasación tool used in Spain | License ~€200/mes |
| **PDF generation (Puppeteer/wkhtmltopdf)** | Generar informes好看的 | Gratis (self-hosted) |
| **Supabase / PostgreSQL** | Base de datos expedientes | ~€25/mes |
| **Notion / Baserow** | Gestión de clientes y seguimiento | Gratis-€8/mes |

### Stack mínimo viable (MVP)
- OpenClaw (core)
- Sede Electrónica Catastro (gratis)
- INE datos abiertos (gratis)
- Supabase (€25/mes)
- Puppeteer para PDFs (gratis)
- **Inversión inicial desarrollo propio:** ~€3.000-8.000 (si se externaliza)
- **Mantenimiento:** ~€500-1.000/mes

---

## 5. FASES DE IMPLEMENTACIÓN

### Fase 1: MVP — Agente de Valoración Aproximada (Semanas 1-4)
**Objetivo:** Tener un chatbot funcional que responda a consultas de valoración aproximada.

**Pasos:**
1. Configurar OpenClaw con canal Telegram (o web)
2. Crear agente de valoración con prompt especializado
3. Integrar llamadas a API del Catastro (reference catastral → datos)
4. Integrar consulta básica de comparables (web scraping o API)
5. Generar informe PDF básico con disclaimer
6. Testing interno
7. Lanzamiento limitado (5-10 clientes piloto)

**Entregable:** Bot funcionando con 5-10 informes de prueba.

**Coste fase 1:** ~€500-1.500 (solo tiempo de configuración + APIs)

---

### Fase 2: Agente de Soporte al Tasador (Semanas 5-8)
**Objetivo:** El tasador recibe un dossier automático antes de cada visita.

**Pasos:**
1. Diseñar la estructura del dossier (qué datos debe contener)
2. Crear agente que reúna: antecedentes, cargas, comparables, fotos
3. Integrar con Idealista API (o scraping avanzado si no hay API)
4. Crear plantilla de dossier (PDF)
5. Integrar con Valtec/OpenTas si posible (exportar datos)
6. Test con 2-3 tasadores durante 2 semanas

**Entregable:** Dossier pre-visita generado automáticamente.

**Coste fase 2:** ~€1.000-3.000 (integraciones + templates)

---

### Fase 3: Agente de Reclamaciones Catastrales (Semanas 9-12)
**Objetivo:** Análisis automático + borrador de alegación.

**Pasos:**
1. Diseñar lógica de evaluación (ratio VC/VM, umbrales por municipio)
2. Crear agente de análisis catastral
3. Integrar con más fuentes (datos fiscales, registros)
4. Generar borrador de alegación con estructura legal correcta
5. Crear workflow de revisión por abogado (si se necesita)
6. Test con 10-20 expedientes reales

**Entregable:** Agente que produce alegaciones borrador en <15 min.

**Coste fase 3:** ~€2.000-5.000 (lógica + integración + testing)

---

### Fase 4: Escalado e Integración (Meses 4-6)
**Objetivo:** Conectar con sistemas existentes y escalar.

**Pasos:**
1. Integración con Valtec/OpenTas/Tecoh (exportación automática)
2. Dashboard de métricas (cuántas valoraciones, tiempo ahorrado, precisión)
3. Base de datos de históricos para mejorar modelos internos
4. Chatbot web para captación de leads (valoración aproximada como lead gen)
5. Conexión con CRM (HubSpot, Pipedrive, Notion)
6. Optimización continua basada en feedback

**Coste fase 4:** ~€3.000-8.000 + mantenimiento €500-1.000/mes

---

## 6. COSTE ESTIMADO

### Inversión inicial total: €6.500 — €17.500

| Concepto | Rango |
|----------|-------|
| Configuración OpenClaw | €0-500 |
| Desarrollo agente valoración (fase 1) | €500-1.500 |
| Desarrollo agente soporte tasador (fase 2) | €1.000-3.000 |
| Desarrollo agente catastral (fase 3) | €2.000-5.000 |
| Integraciones + escalado (fase 4) | €3.000-8.000 |

### Costes recurrentes mensuales

| Concepto | Coste mensual |
|----------|--------------|
| OpenClaw (plan profesional) | €29-99 |
| Idealista API | €0-300 |
| Supabase (DB) | €25 |
| Dominio + hosting docs | €10 |
| Mantenimiento técnico (4h/mes) | €200-400 |
| **Total mensual** | **€264-834** |

### Coste por valoración (a modo de referencia)

Si la empresa hace **100 valoraciones/mes**:
- Coste infraestructura: ~€5-8 por valoración
- Coste con tasador manual: ~€60-120 por valoración (tiempo)
- **Ahorro por valoración: €55-112**

---

## 7. LIMITACIONES Y AVISOS LEGALES

### Lo que un agente IA PUEDE hacer legítimamente:

✅ **Recopilar datos** de fuentes públicas y APIs oficiales (Catastro, INE, Idealista)
✅ **Generar informes de valoración aproximada** con disclaimer explícito de que no es una tasación oficial
✅ **Preparar borrador de alegaciones** para revisión humana
✅ **Buscar comparables** y presentar datos de mercado
✅ **Resumir y estructurar información** para un tasador homologado
✅ **Calcular ratios** (VC/VM, precio m²) y compararlos con medias

### Lo que un agente IA NO puede hacer:

❌ **Firmar una tasación oficial** — requiere tasador homologado por el Banco de España
❌ **Emitir un certificado de tasación** válido para una entidad financiera
❌ **Asegurar la precisión** de una valoración — siempre debe haber revisión humana
❌ **Acceder a datos protegidos** sin consentimiento del titular (RGPD)
❌ **Intervenir en procedimientos judiciales** sin abogado habilitado

### Disclaimer obligatorio para todo informe de IA:

```
AVISO LEGAL: Este documento es una VALORACIÓN APROXIMADA generada por 
inteligencia artificial a partir de datos públicos. NO CONSTITUYE UNA 
TASACIÓN OFICIAL ni tiene validez legal para operaciones financieras, 
judiciales o administrativas. Para una tasación con efectos legales, 
consulte con un tasador homologado conforme al Real Decreto 775/1997.
Los datos utilizados proceden de fuentes públicas (Catastro, INE, 
portales inmobiliarios) y pueden contener inexactitudes. EG Consultoría 
declina toute responsabilidad por decisiones tomadas en base a este 
informe sin verificación profesional.
```

### Marco normativo clave

| Norma | Qué regula |
|-------|-----------|
| **Real Decreto 775/1997** | Homologación de tasadores — quién puede tasar para entidades financieras |
| **Orden ECO/805/2003** | Normas de valoración de bienes inmuebles (valor tasable, mercado) |
| **Ley Hipotecaria** | Funciones del Registro de la Propiedad |
| **Ley del Catastro** (RDLeg 1/2004) | Funciones y procedimientos catastrales |
| **RGPD** (UE 2016/679) | Protección de datos personales de clientes e inmuebles |
| **Ley 18/2020** (Madrid) | 일부... |

---

## 8. ROI ESTIMADO

### Situación actual (empresa media: 5 tasadores, 80 expedientes/mes)

| Actividad | Tiempo actual/mes | Tiempo con IA/mes | Ahorro |
|-----------|-------------------|-------------------|--------|
| Búsqueda de datos pre-visita | 80 × 50 min = 4.000 min | 80 × 8 min = 640 min | **3.360 min** |
| Valoraciones aproximadas | 40 × 60 min = 2.400 min | 40 × 10 min = 400 min | **2.000 min** |
| Revisión catastral | 15 × 90 min = 1.350 min | 15 × 15 min = 225 min | **1.125 min** |
| Documentación varia | 20 × 30 min = 600 min | 20 × 10 min = 200 min | **400 min** |
| **TOTAL** | **~8.350 min** | **~1.465 min** | **~6.885 min** |

**~115 horas/mes ahorradas** = ~14 días laborables/mes para 5 tasadores

### Beneficios adicionales (intangibles)
- **Respuesta más rápida** al cliente → más conversiones
- **Datos más completos** → menos visitas de vuelta → ahorro en desplazamiento
- **Base de datos histórica** → aprende de cada expediente
- **Disponibilidad 24/7** para consultas básicas
- **Mayor volumen** posible sin contratar más personal

### Payback

| Concepto | Valor |
|----------|-------|
| Coste implementación total | €6.500-17.500 |
| Ahorro mensual (115h × €35/hora equivalent) | ~€4.000/mes |
| **Payback** | **2-4 meses** |
| Ahorro anual (año 2+) | ~€48.000/año |

---

## 9. RIESGOS Y MITIGACIONES

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|---------|-----------|
| Error en valoración aproxima da causa perjuicio | Media | Alto | Disclaimer prominente + revisión humana obligatoria |
| Acceso a datos personales (RGPD) | Media | Alto | No almacenar datos sensibles sin consentimiento |
| Fallo en API del Catastro | Baja | Medio | Tener fuentes alternativas (INE, Idealista) |
| IA genera alegación incorrecta | Media | Medio | Revisión por profesional antes de presentar |
| Cambios legales en el proceso catastral | Baja | Medio | Actualizar prompts cuando cambie la normativa |
| Dependencia de un solo canal (Idealista) | Media | Bajo | Multiples fuentes de datos |

---

## 10. PRÓXIMOS PASOS INMEDIATOS

1. **Esta semana:** Validar este plan con el equipo directivo
2. **Semana 2:** Elegir el caso de uso piloto (recomiendo: **valoración aproximada**)
3. **Semana 3:** Configurar OpenClaw y crear cuenta de API del Catastro
4. **Semana 4:** Primer prototipo funcional del agente de valoración
5. **Mes 2:** Test con 10 clientes reales + medir tiempo y satisfacción
6. **Mes 3:** Lanzar agente de soporte al tasador
7. **Mes 4:** Lanzar agente de reclamaciones catastrales

---

*Documento preparado con conocimiento del sector de valoración inmobiliaria española. Datos de APIs y precios sujetos a verificación actual.*
