# WIREFRAME — Pantallas clave de la web inmobiliaria

> Descripción textual de cada pantalla: estructura, componentes, contenido y comportamiento. No incluye detalles de color (ver PLAN.md).

---

## P0 — Pantallas público (usuario anónimo)

---

### P0.1 HOME (Inicio)

**URL:** `/`

**Objetivo:** Transmitir profesionalidad, facilitar búsqueda rápida, mostrar inmuebles destacados.

**Estructura:**

```
┌─────────────────────────────────────────────────────┐
│  HEADER (sticky, backdrop-blur)                    │
│  [Logo]  Inicio  Comprar  Alquiler  Vender  Contacto │
│                              [🔑 Acceder] [+Publicar]│
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  HERO (100vh - header, imagen de fondo con overlay) │
│                                                     │
│        "Tu próximo hogar está aquí"                │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │ [Comprar ▾] [Piso ▾] [📍 Ciudad o zona...]  │   │
│  │  Precio: [Min ▾] — [Max ▾]                   │   │
│  │  m²: [Min ▾] — [Max ▾]                      │   │
│  │              [🔍 Buscar]                    │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  --- CONTADOR ---                                   │
│  +250 inmuebles  |  +180 clientes satisfechos  |   │
│  15 años de experiencia                              │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  SECCIÓN: "Destacados del mes"                      │
│  ─────────────────────────────────────────────────  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │  [FOTO]  │  │  [FOTO]  │  │  [FOTO]  │        │
│  │──────────│  │──────────│  │──────────│        │
│  │ [ALQUILER]│  │ [VENTA]  │  │ [VENTA]  │        │
│  │ Piso c/   │  │ Chalet   │  │ Ático    │        │
│  │ Cervantes │  │ c/ Mar   │  │ c/ Sol   │        │
│  │           │  │          │  │          │        │
│  │ 95 m² 3d  │  │ 180m² 4d │  │ 75m² 2d  │        │
│  │ €850/mes  │  │ €295.000 │  │ €210.000 │        │
│  │ [Ver →]   │  │ [Ver →]  │  │ [Ver →]  │        │
│  └──────────┘  └──────────┘  └──────────┘        │
│                                                     │
│           [←  1  2  3  →]                          │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  SECCIÓN: "¿Por qué elegirnos?"                    │
│  ─────────────────────────────────────────────────  │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐    │
│  │  🏆         │ │  🤝         │ │  📍         │    │
│  │ Experiencia│ │ Atención   │ │ Zona        │    │
│  │ +15 años en │ │ personalizada│ │ Conocemos   │    │
│  │ la zona     │ │ cada cliente│ │ cada barrio │    │
│  └────────────┘ └────────────┘ └────────────┘    │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  FOOTER                                             │
│  [Logo]                                            │
│  Calle Ejemplo 12, Madrid  │  📞 +34 912 345 678  │
│  info@inmobiliaria.es  │  Horarios: L-V 9-20h     │
│  ────────────────────────────────────────────────  │
│  Aviso Legal | Política de Privacidad | Cookies    │
│  © 2025 Inmobiliaria Ejemplo S.L.  CIF: B-12345678│
└─────────────────────────────────────────────────────┘
```

**Comportamiento:**
- Hero con imagen de fondo ( Next.js Image con priority).
- Buscador: inputs con validación, autocomplete ubicación (Nominatim).
- Cards destacadas: lazy-load con skeleton en loading.
- Scroll suave al hacer clic en "Ver" (scroll a sección o navegación).

---

### P0.2 LISTADO DE INMUEBLES

**URL:** `/inmuebles` (y `/inmuebles?operacion=venta&ciudad=madrid&...`)

**Objetivo:** Mostrar catálogo filtrable con suficiente información para que el usuario quiera clickar.

**Estructura:**

```
┌─────────────────────────────────────────────────────┐
│  HEADER (mismo que home)                           │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  BREADCRUMB: Inicio > Inmuebles > Madrid           │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  PANEL DE FILTROS (collapsible en móvil)           │
│  ─────────────────────────────────────────────────  │
│  Tipo: [Todas ▾] [Piso] [Chalet] [Ático] [Local]   │
│  Operación: [●] Alquiler  [●] Venta  [●] Todos    │
│  Precio: [────●────────●────] €500 — €500.000     │
│  m²:    [────●────────●────] 30 — 300 m²          │
│  Hab:   [Cualquiera] [1] [2] [3] [4+]              │
│  Ciudad: [____________] (autocomplete)            │
│                                                      │
│  [Borrar filtros]  [🔍 Aplicar]                    │
│                                                      │
│  [Vista lista] [Vista mapa] (toggle)               │
│                                                      │
│  Ordenar: [Más recientes ▾]                        │
│  42 inmuebles encontrados                          │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  GRID DE CARDS (3 cols desktop, 2 tablet, 1 móvil) │
│  ─────────────────────────────────────────────────  │
│  ┌─────────────────────────────────────────────┐  │
│  │ [FOTO ppal]                    [ALQUILER]    │  │
│  │                                      [♡]    │  │
│  │─────────────────────────────────────────────│  │
│  │ €950/mes                      📍 Chamberí   │  │
│  │ Piso luminoso en Chamberí                   │  │
│  │ 85 m²  │  2 hab  │  1 baño  │  🅿️  🛗       │  │
│  │                               [Ver detalle →]│  │
│  └─────────────────────────────────────────────┘  │
│                                                      │
│  [Card 2...] [Card 3...] [Card 4...]               │
│                                                      │
│           [←  1  2  3 ... 5  →]                    │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  FOOTER                                             │
└─────────────────────────────────────────────────────┘
```

**Comportamiento:**
- Filtros actualizan URL (query params) → shareable links.
- Paginación: 12 items por página, scroll suave al cambiar.
- Toggle lista/mapa: mapa usa Leaflet con marcadores, al clickar abre popup con mini-card.
- Favoritear: guarda en localStorage (no requiere login en esta fase).
- Loading: skeleton cards con shimmer animation.

---

### P0.3 DETALLE DE INMUEBLE

**URL:** `/inmuebles/[slug]` o `/inmuebles/[id]`

**Objetivo:** Toda la información del inmueble + CTA de contacto.

**Estructura:**

```
┌─────────────────────────────────────────────────────┐
│  HEADER                                            │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  BREADCRUMB: Inicio > Inmuebles > Madrid > Piso... │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  GALERÍA DE FOTOS                                  │
│  ─────────────────────────────────────────────────  │
│  ┌─────────────────────────────────────────────┐  │
│  │                                              │  │
│  │         [FOTO PRINCIPAL]                     │  │
│  │                                              │  │
│  │  [1] [2] [3] [4] [5] →  (thumbnails)         │  │
│  │                                              │  │
│  │  3 / 15  [⛶ Fullscreen]  [▶ Play video]   │  │
│  └─────────────────────────────────────────────┘  │
│                                                      │
│  REF: P-2025-0042              [🔗 Compartir] [♡]  │
└─────────────────────────────────────────────────────┘

┌───────────────────────┬───────────────────────────┐
│  INFO PRINCIPAL       │  WIDGET CONTACTO          │
│  ─────────────────    │  ─────────────────────── │
│                       │                           │
│  €295.000             │  ┌───────────────────────┐│
│  (Impuestos no incl.) │  │ ¿Te interesa?         ││
│                       │  │                       ││
│  🏠 Piso en venta      │  │ Nombre: [__________] ││
│  📍 c/ Cervantes 23   │  │ Email:  [__________] ││
│     Chamberí, Madrid   │  │ Tfno:   [__________] ││
│                       │  │                       ││
│  ┌───────────────┐    │  │ Tipo consulta:        ││
│  │ 85 m²  │  3 hab│    │  │ [Solicitar info ▾]    ││
│  │ 72 m² útil    │    │  │                       ││
│  │ 2 baños │ 2ª pl│    │  │ Mensaje (opcional):  ││
│  │ Ascensor 🛗   │    │  │ [________________]   ││
│  │ Parking 🅿️     │    │  │                       ││
│  └───────────────┘    │  │ ☑ Acepto [privacidad] ││
│                       │  │                       ││
│  ──────────────────   │  │  [Enviar mensaje]     ││
│  💰 FINANCIACIÓN      │  └───────────────────────┘│
│  Simulador hipoteca   │                           │
│  [Calcular →]         │  📞 912 345 678           │
│                       │  WhatsApp: [Escribir →]   │
│  ──────────────────   │                           │
│  📋 DESCARGAS         │                           │
│  [📄 Ficha PDF]       │                           │
│  [📄 Certificado E.]   │                           │
└───────────────────────┴───────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  DESCRIPCIÓN                                       │
│  ─────────────────────────────────────────────────  │
│  Bellísimo piso exterior de 85m² situado en...   │
│  (texto completo del inmueble)                     │
│                                                      │
│  - Cocina independiente equipada                   │
│  - Suelo de parqué original                        │
│  - Ventanas de climalit                            │
│  ...                                                │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  CARACTERÍSTICAS                                   │
│  ─────────────────────────────────────────────────  │
│  Tipo: Piso          │  Estado: Buen estado        │
│  m² útiles: 72       │  Orientación: Sur          │
│  Planta: 2ª          │  Ascensor: Sí              │
│  habitaciones: 3      │  Parking: Sí (incluido)    │
│  Baños: 2            │  Trastero: No              │
│  Año construcción:   │  Terraza: No               │
│  1978                │  Aire acond.: No           │
│  ─────────────────────────────────────────────────  │
│  Cert. Energético: D   (ver certificado)           │
│  Emisiones: D                                   │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  MAPA                                               │
│  ─────────────────────────────────────────────────  │
│  ┌─────────────────────────────────────────────┐  │
│  │            [MAPA LEAFLET]                   │  │
│  │          📍 marcador en ubicación           │  │
│  │                                              │  │
│  │  [🛰️ Ver en Google Maps]                    │  │
│  └─────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  INMUEBLES SIMILARES                               │
│  ─────────────────────────────────────────────────  │
│  [Card] [Card] [Card]                              │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  FOOTER                                            │
└─────────────────────────────────────────────────────┘
```

**Comportamiento:**
- Galería: swipe en móvil, flechas en desktop, lightbox fullscreen.
- Contador de vistas se incrementa en servidor al cargar.
- Widget contacto: validación JS + servidor, loading state en submit.
- PDF: generado dinámicamente con datos del inmueble.
- Similar: query aleatoria de 3 inmuebles mismo tipo + ciudad.

---

### P0.4 PÁGINA DE CONTACTO

**URL:** `/contacto`

```
┌─────────────────────────────────────────────────────┐
│  HEADER                                            │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  HERO INTERIOR: "Contacta con nosotros"            │
│  (imagen sutil, no fullscreen)                     │
└─────────────────────────────────────────────────────┘

┌────────────────────────┬───────────────────────────┐
│  FORMULARIO            │  INFO DE CONTACTO         │
│  ────────────────────   │  ──────────────────────── │
│                        │                           │
│  Nombre*: [__________] │  📍 Calle Ejemplo 12      │
│  Email*:  [__________] │     28010 Madrid          │
│  Tfno:   [__________] │                           │
│                        │  📞 +34 912 345 678       │
│  Asunto: [____________]│  ✉  info@midominio.es     │
│  [ General ▾]          │                           │
│                        │  🕐 L-V: 9:00 - 20:00      │
│  Mensaje*:             │     S: 10:00 - 14:00      │
│  [________________]   │                           │
│  [________________]   │  ┌───────────────────────┐│
│  [________________]   │  │ [Google Maps embed]  ││
│  [________________]   │  │                       ││
│                        │  └───────────────────────┘│
│  ☑ Acepto [privacidad]│                           │
│                        │                           │
│  [Enviar mensaje]     │                           │
└────────────────────────┴───────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  FOOTER                                            │
└─────────────────────────────────────────────────────┘
```

---

## P1 — Pantallas Admin

---

### P1.1 LOGIN ADMIN

**URL:** `/admin/login`

```
┌─────────────────────────────────────────────────────┐
│  [Logo empresa]                                    │
│                                                      │
│  ┌───────────────────────────────────────────────┐ │
│  │                                               │ │
│  │       Panel de Administración                │ │
│  │                                               │ │
│  │       Email:    [____________________]        │ │
│  │       Contraseña: [____________________]     │ │
│  │                                               │ │
│  │              [🔓 Iniciar sesión]             │ │
│  │                                               │ │
│  │       ¿Olvidaste tu contraseña?              │ │
│  │                                               │ │
│  └───────────────────────────────────────────────┘ │
│                                                      │
│  ← Volver al sitio web                             │
└─────────────────────────────────────────────────────┘
```

**Comportamiento:**
- Supabase Auth (email/password).
- Redirect a `/admin` tras login exitoso.
- Rate limiting en servidor (max 5 intentos).

---

### P1.2 DASHBOARD ADMIN

**URL:** `/admin`

**Objetivo:** Vista general del estado del negocio.

```
┌─────────────────────────────────────────────────────┐
│  ADMIN HEADER (diferente del público)               │
│  [Logo] Inmobiliaria Admin  │  [🔔 3] [Avatar ▾]  │
│  ──────────────────────────────────────────────── │
│  Dashboard | Inmuebles | Leads | Ajustes | Salir  │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  KPIs (4 cards en row)                             │
│  ─────────────────────────────────────────────────  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ │
│  │ 🏠 24     │ │ 👁 1.243 │ │ 📧 8     │ │ 📊 32% │ │
│  │ Activos  │ │ Visitas  │ │ Leads    │ │ Conv.  │ │
│  │           │ │ (este mes│ │ (nuevos) │ │ leads/ │ │
│  │           │ │           │ │           │ │ visita │ │
│  │ [+3 este │ │ [vs mes   │ │ [2 sin   │ │ [vs mes│ │
│  │  mes]     │ │  pasado]  │ │  atender]│ │  pas.] │ │
│  └──────────┘ └──────────┘ └──────────┘ └────────┘ │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  ÚLTIMOS LEADS                                     │
│  ─────────────────────────────────────────────────  │
│  ┌─────────────────────────────────────────────┐  │
│  │ [!nuevo] María G. — Piso c/ Cervantes      │  │
│  │         Quiere visitar. Tfno: 600 XXX XXX │  │
│  │         Hace 2 horas  │  [→ Asignar]       │  │
│  ├─────────────────────────────────────────────┤  │
│  │ Juan R. — Chalet en Alcobendas              │  │
│  │        Solicitud de info. hace 1 día       │  │
│  │        Atendido por: Ana  │  [→ Ver]       │  │
│  ├─────────────────────────────────────────────┤  │
│  │ ...                                         │  │
│  └─────────────────────────────────────────────┘  │
│                                                      │
│  [Ver todos los leads →]                           │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  ÚLTIMOS INMUEBLES AÑADIDOS                        │
│  ─────────────────────────────────────────────────  │
│  ┌─────────────────────────────────────────────┐  │
│  │ 🟢 P-2025-0045 — Ático c/ Sol, Madrid        │  │
│  │    Venta · €310.000 · Creado hoy            │  │
│  │    [→ Editar]  [→ Preview]  [👁 12 visitas] │  │
│  ├─────────────────────────────────────────────┤  │
│  │ 🟡 P-2025-0044 — Local c/ Gran Vía           │  │
│  │    Alquiler · €1.200/mes · Hace 3 días      │  │
│  │    [→ Editar]  [→ Preview]                 │  │
│  └─────────────────────────────────────────────┘  │
│                                                      │
│  [Gestionar inmuebles →]                           │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  GRÁFICA DE VISITAS (últimos 30 días)              │
│  ─────────────────────────────────────────────────  │
│  📈 [gráfico de barras simple con recharts]         │
│  Visitas: ▓▓▓▓▓▓▓▓▓▓░░ 1.243 total                 │
│  Inmueble más visto: Piso c/ Cervantes (234 visitas)│
└─────────────────────────────────────────────────────┘
```

**Comportamiento:**
- Cards con tooltips al hover.
- Gráfico con Recharts (ligero).
- Refresh de datos cada 60s (React Query staleTime).
- Notificación toast cuando llega lead nuevo (Supabase Realtime).

---

### P1.3 LISTADO DE INMUEBLES (ADMIN)

**URL:** `/admin/inmuebles`

```
┌─────────────────────────────────────────────────────┐
│  ADMIN HEADER                                      │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  [🔍 Buscar por referencia, título, ciudad...]     │
│                                                      │
│  Filtros: [Estado ▾] [Tipo ▾] [Operación ▾]        │
│                                                      │
│  [🟢 Activos: 18] [🟡 Borradores: 3] [🔴 Vendidos: 5]│
│                                                      │
│  [+ Añadir inmueble]                               │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  TABLA DE INMUEBLES                                │
│  ─────────────────────────────────────────────────  │
│  ☐  │ Ref    │ Título        │ Tipo  │ Op  │Precio│  │
│  ───┼────────┼───────────────┼───────┼─────┼──────│  │
│  ☐  │0045    │ Ático c/ Sol  │ Ático │ Vta │310k │  │
│  ☐  │0044    │ Local Gran Vía│ Local │ Alq │1.2k │  │
│  ☐  │0043    │ Piso Chamberí │ Piso  │ Vta │295k │  │
│  ...│        │               │       │     │      │  │
│                                                      │
│  [← 1  2  3 →]  Mostrando 1-20 de 42              │
└─────────────────────────────────────────────────────┘
```

**Acciones por fila:** Editar, Duplicar, Preview, Eliminar (confirmación modal).

---

### P1.4 FORMULARIO ALTA/EDICIÓN DE INMUEBLE

**URL:** `/admin/inmuebles/nuevo` o `/admin/inmuebles/[id]/editar`

```
┌─────────────────────────────────────────────────────┐
│  ADMIN HEADER                                      │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  ← Volver a inmuebles                              │
│  [Modo: NUEVO INMUEBLE / EDITANDO: P-2025-0045]   │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  TABS: [Datos] [Fotos] [Mapa] [SEO]                │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  ── TAB: DATOS BÁSICOS ──────────────────────────── │
│                                                      │
│  Referencia*: [P-2025-____] (auto o manual)        │
│  Título*: [Piso luminoso en Chamberí___________]    │
│                                                      │
│  Operación*: [●] Venta  [○] Alquiler  [○] Ambos  │
│  Tipo*: [Piso ▾] (dropdown)                        │
│                                                      │
│  Precio*: [_________] €                           │
│  Gastos comunidad: [_________] €/mes (opcional)    │
│  Impuestos: [ ] Precio con IVA                     │
│                                                      │
│  Descripción*:                                      │
│  ┌─────────────────────────────────────────────┐  │
│  │ [textarea, 500-3000 chars]                   │  │
│  │                                             │  │
│  └─────────────────────────────────────────────┘  │
│                                                      │
│  ── UBICACIÓN ──────────────────────────────────  │
│  Dirección: [c/ Cervantes 23___________________]  │
│  Ciudad*: [Madrid______________________________]  │
│  Provincia*: [Madrid__________________________]  │
│  CP: [28010____]                                   │
│  [📍 Pinchar en mapa para ubicar]                  │
│  ┌─────────────────────────────────────────────┐  │
│  │         [MAPA LEAFLET con draggable marker] │  │
│  │              📍 marcador                     │  │
│  └─────────────────────────────────────────────┘  │
│  Lat: [40.4342]  Lng: [-3.6971] (editables)       │
│                                                      │
│  ── CARACTERÍSTICAS ───────────────────────────── │
│  m² construidos: [___]  m² útiles: [___]         │
│  m² parcela: [___] (solo chalets)                  │
│  Habitaciones: [2 ▾]  Baños: [1 ▾]  Aseo: [0▾]   │
│  Plantas: [1 ▾]  Planta número: [2___]            │
│  Año construcción: [____]                          │
│  Orientación: [Sur ▾]                              │
│  Certificado energético: [D ▾]                     │
│  Emisiones: [D ▾]                                  │
│                                                      │
│  Extras (checkboxes):                              │
│  [ ] Ascensor  [ ] Parking  [ ] Trastero          │
│  [ ] Terraza  [ ] Balcón  [ ] Jardín               │
│  [ ] Piscina  [ ] Aire acondicionado               │
│  [ ] Calefacción  [ ] Chimenea  [ ] Domótica       │
│                                                      │
│  ── VÍDEO ──────────────────────────────────────── │
│  URL YouTube/Vimeo: [https://...]                  │
│  [Vista previa del embed]                           │
│                                                      │
│  ── ESTADO ────────────────────────────────────── │
│  Estado*: [Borrador ▾]                             │
│           [Borrador] → No visible al público       │
│           [Publicado] → Visible                    │
│           [Reservado] → No visible, "Reservado"    │
│           [Vendido/Alquilado] → Archivado          │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  ── TAB: FOTOS ──────────────────────────────────── │
│                                                      │
│  Arrastra imágenes aquí o [haz clic para subir]    │
│  Formatos: JPG, PNG, WEBP. Máx 10MB cada una.       │
│                                                      │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐        │
│  │ ☐  │ │ ☐  │ │ ☐  │ │ ☐  │ │ ☐  │ │ + │        │
│  │img1│ │img2│ │img3│ │img4│ │img5│ │upload│        │
│  │ ⭐ │ │    │ │    │ │    │ │    │ │      │        │
│  └────┘ └────┘ └────┘ └────┘ └────┘ └────┘        │
│  (drag to reorder, ⭐= principal)                  │
│                                                      │
│  5 fotos · 12MB / 50MB máximo                      │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  ── TAB: MAPA ───────────────────────────────────── │
│  (Repite ubicación editable visualmente)            │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  ── TAB: SEO ────────────────────────────────────── │
│                                                      │
│  Slug (URL): [/inmuebles/piso-chamberi-cervantes] │
│  Meta título: [Piso en Chamberí - 3 hab - 295.000€│
│  Meta descripción: [___[__________________________│
│  Schema markup: (auto-generado, editable si quieres)│
│                                                      │
│  Preview Google:                                   │
│  ┌─────────────────────────────────────────────┐   │
│  │ Título (60 chars máx)                       │   │
│  │ https://midominio.es/inmuebles/piso-chambe..│   │
│  │ Descripción (160 chars máx)...              │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  [💬 Guardar como borrador]  [💬 Guardar y publicar│
└─────────────────────────────────────────────────────┘
```

**Comportamiento:**
- Auto-save cada 30s (debounced).
- Preview en tiempo real del inmueble público (nueva pestaña).
- Drag & drop imágenes con `react-dnd` o similar.
- Coordenadas del mapa se auto-llenan al arrastrar el pin.

---

### P1.5 GESTIÓN DE LEADS

**URL:** `/admin/leads`

```
┌─────────────────────────────────────────────────────┐
│  ADMIN HEADER                                      │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  📧 Leads                                          │
│                                                      │
│  [🔴 Nuevos (8)] [🟡 En proceso (5)] [🟢 Atendidos(23)]│
│                                                      │
│  FILTROS: [Desde ▾] [Hasta ▾] [Agente ▾]           │
│                                                      │
│  ┌─────────────────────────────────────────────┐  │
│  │ [!nuevo] María García                       │  │
│  │ 📞 600 123 456  ✉  maria@email.com          │  │
│  │ Interesada en: Piso c/ Cervantes (REF:0043) │  │
│  │ "Me gustaría visitar este viernes..."       │  │
│  │ Hace 2h · Web · [Asignar a: Ana ▾] [→ Ver]  │  │
│  ├─────────────────────────────────────────────┤  │
│  │ Juan Rodríguez                             │  │
│  │ 📞 600 789 012  ✉  juan@email.com          │  │
│  │ Quiere vender: Casa en Fuenlabrada          │  │
│  │ Hace 1 día · Web · Asignado: Pedro          │  │
│  │ [→ Ver]                                    │  │
│  └─────────────────────────────────────────────┘  │
│                                                      │
│  [Exportar CSV]                                    │
└─────────────────────────────────────────────────────┘
```

**Detalle lead (modal o página):** Historial de comunicación, datos del inmueble asociado, notas internas.

---

## P2 — Mobile

### P2.1 HOME MÓVIL

- Hero: imagen ocupa 60vh, buscador debajo en vez de encima.
- Cards: 1 columna, swipe horizontal de categorías.
- Menú: hamburger → drawer full-screen.
- Footer: acordeón con secciones colapsables.

### P2.2 LISTADO MÓVIL

- Filtros: drawer desde abajo (bottom sheet) con "Aplicar" sticky.
- Cards: 1 columna, imágenes 16:9.
- Mapa: pantalla completa con toggle "Ver lista".

### P2.3 DETALLE MÓVIL

- Galería: fullscreen swipeable con indicador de página.
- Sticky footer con precio + "Contactar" (CTA flotante).
- Mapa: 50vh de altura, collapsible.
- Widget contacto: sticky en bottom sheet.

---

## Notas de implementación UI

1. **Skeleton loading:** Para todas las secciones con datos async.
2. **Toast notifications:** Para feedback de acciones (guardado, error).
3. **Modales de confirmación:** Para eliminar, despublicar.
4. **Drag & drop:** Para reorder de imágenes y prioridad.
5. **Progresivo:** No bloquear al usuario por falta de datos opcionales.
6. **Graceful degradation:** Si mapa falla → mostrar dirección en texto.
7. **Offline:** Service Worker para caching básico de imágenes.
