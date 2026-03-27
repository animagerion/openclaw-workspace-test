# PLAN — Web de Inmobiliaria Local

> Documento maestro: diseño, arquitectura, funcionalidades, stack, base de datos, integraciones, costes, fases y requisitos legales.

---

## 1. DISEÑO Y UX

### 1.1 Identidad Visual

**Sector:** Inmobiliario (compra/venta/alquiler de viviendas en España).

**Moodboard:**
- Limpio, profesional, confiable.
- Espacios amplios, fotos de calidad como protagonistas.
- Tono: cercano pero serio, no frío corporativo ni desenfadado.
- Inspiración: Houzez (ThemeForest), Solid Realtors (Webflow), portales como Tecnocasa y Solvia.

### 1.2 Paleta de Colores

| Rol | Color | Hex | Uso |
|-----|-------|-----|-----|
| Primario | Azul profundo | `#1B3A5C` | Headers, CTA principales, texto destacado |
| Secundario | Dorado/Ámbar | `#C9A84C` | Acentos, badges "Destacado", iconos |
| Fondo | Blanco hueso | `#FAFAF8` | Página principal |
| Superficie | Gris muy claro | `#F2F2F0` | Cards, secciones alternas |
| Texto | Gris oscuro | `#2D2D2D` | Cuerpo de texto |
| Texto secundario | Gris medio | `#6B7280` | Metadatos, descripciones cortas |
| Éxito | Verde | `#16A34A` | Pills "Disponible", confirmaciones |
| Alerta | Rojo suave | `#DC2626` | Pills "Vendido", errores |

### 1.3 Tipografía

| Rol | Fuente | Fallback | Uso |
|-----|--------|----------|-----|
| Display | **Playfair Display** | Georgia, serif | Títulos principales, nombres de la empresa |
| Cuerpo | **Inter** | system-ui, sans-serif | Textos, labels, body copy |
| Mono/Datos | **JetBrains Mono** | monospace | Precios, metros cuadrados, referencias |

**Escala tipográfica:**
- H1: 48px / 1.1 lh (hero)
- H2: 36px / 1.2 lh (secciones)
- H3: 24px / 1.3 lh (cards, títulos de página)
- Body: 16px / 1.6 lh
- Small: 13px / 1.4 lh (metadatos)

### 1.4 Layout Recomendado

**Grid:** 12 columnas, gap 24px, max-width 1280px centrado.

**Estructura de página (público):**
```
Header (sticky, blur backdrop)
  ├── Logo
  ├── Nav: Inicio | Comprar | Alquiler | Vender | Contacto
  └── CTA: "Ver inmuebles" / Login admin

Hero (full-width, imagen de fondo con overlay + buscador principal)

Filtros rápidos (sticky bajo hero al hacer scroll)
  ├── Tipo operación (comprar/alquilar)
  ├── Tipo inmueble (piso, chalet, local...)
  ├── Ubicación (autocomplete con Nominatim/TomTom)
  ├── Rango precio (slider dual)
  ├── m² (slider dual)
  └── Habitaciones (selector)

Listado de inmuebles (grid 3 columnas desktop, 2 tablet, 1 móvil)
  └── Cards con foto principal, precio, ubicación, m², habitaciones

Mapa (opcional, Leaflet/Mapbox) junto al listado (desktop)

Footer
  ├── Datos de contacto, redes, horarios
  ├── Enlaces legales (RGPD, cookies, aviso legal)
  └── Logo + copyright
```

### 1.5 Componentes UI Clave

- **PropertyCard:** foto (aspect 4:3), badge operación, precio grande, dirección, iconos m²/hab/baños, botón "Ver detalle"
- **SearchBar:**input con autocompletado de ubicación, dropdown de sugerencias
- **FilterPanel:** colapsable en móvil, sticky en desktop
- **PropertyGallery:** lightbox con swipe, contador de fotos, thumbnail strip
- **MapMarker:** cluster en zoom out, popup con mini-card al clickar
- **ContactForm:** nombre, email, teléfono, mensaje, checkbox RGPD
- **AdminTable:** sortable, paginada, filtros, acciones (editar/eliminar/publicar)
- **Dashboard widgets:** stats cards (total inmuebles, visitas, leads, conversion)

### 1.6 Responsive

- Mobile-first CSS (Tailwind CSS o CSS Modules)
- Breakpoints: sm 640px, md 768px, lg 1024px, xl 1280px
- Menú hamburger en móvil
- Cards: 1 columna móvil, 2 tablet, 3 desktop
- Map toggle en listing: "Ver mapa" / "Ver lista"

---

## 2. ARQUITECTURA COMPLETA

### 2.1 Diagrama de flujo de datos

```
[Usuario público]
    │
    ▼
[Frontend: Next.js 14 (App Router)]
    ├── SSR para SEO (getServerSideProps → getServerData)
    ├── SSG para listado (revalidate ISR)
    └── CSR para dashboard admin
    │
    ▼
[Backend API: Next.js API Routes (o NestJS separado)]
    │
    ▼
[Base de datos: PostgreSQL (Supabase o Neon)]
    │
    ├── Auth: Supabase Auth / NextAuth.js
    ├── Storage: Supabase Storage (fotos/videos)
    └── Realtime: Supabase Realtime (notificaciones)

[Servicios externos]
    ├── Idealista API (publicación listings)
    ├── Fotocasa / Kyero (feeds XML/JSON)
    ├── Mapbox / Leaflet (mapas)
    ├── Nodemailer / Resend (email transaccional)
    └── Cloudflare R2 / AWS S3 (CDN assets pesados)
```

### 2.2 Flujo de peticiones

```
Navegador usuario
    │
    ▼ GET /
Next.js → ISR → Devuelve HTML con datos (lista inmuebles destacados)
    │
    ▼ GET /inmuebles?filtros...
Next.js API route → PostgreSQL → JSON → SSG/ISR cache
    │
    ▼ GET /inmuebles/[id]
Next.js → SSG (generateStaticParams) + ISR revalidate=3600
    │
    ▼ POST /api/contact
Next.js API route → valida → guarda en DB → envía email a agente

Admin:
    │
    ▼ GET /admin
Next.js (client, auth requerida) → API routes → DB
    │
    ▼ POST /admin/inmuebles
API route → valida (Zod) → upload imágenes (Storage) → INSERT DB
```

### 2.3 Diagrama de arquitectura (texto)

```
                    ┌──────────────────┐
                    │   Cloudflare CDN  │  (SSL, caché, DDoS)
                    └────────┬──────────┘
                             │
                    ┌────────▼──────────┐
                    │   Vercel / Railway │  (Next.js hosting)
                    │  (Frontend + API)  │
                    └────────┬──────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
    ┌───────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐
    │  Supabase    │  │  Resend /   │  │  Mapbox /   │
    │  PostgreSQL  │  │  Nodemailer │  │  Leaflet    │
    │  + Storage   │  │  (email)    │  │  (maps)     │
    │  + Auth      │  └─────────────┘  └─────────────┘
    └──────────────┘
```

---

## 3. FUNCIONALIDADES

### 3.1 Lado público (usuario anónimo o registrado)

| Funcionalidad | Prioridad | Descripción |
|---|---|---|
| Buscador con filtros | Must | Tipo operación, inmueble, ubicación (autocomplete), precio, m², habitaciones, baños |
| Listado con paginación | Must | Grid de cards, 12-24 por página, ordenación (precio, fecha, m²) |
| Detalle de inmueble | Must | Galería fotos, descripción, características, mapa, contacto |
| Galería de fotos/vídeos | Must | Lightbox, swipe, vídeo YouTube/Vimeo embebido |
| Mapa con ubicación | Should | Leaflet (OpenStreetMap) o Mapbox, marcadores con mini-card |
| Formulario de contacto | Must | Nombre, email, teléfono, mensaje, tipo de consulta, checkbox RGPD |
| Ficha técnica (Ley de Propiedad Horizontal) | Must | Para alquileres: IBI, comunidad, seguro, EPC (certificado energético) |
| Inmuebles destacados | Should | Carousel o sección "Destacados" |
| Búsqueda guardada (alertas) | Should | Email con nuevos inmuebles que cumplan criterios |
| Página "Vender/Alquilar" | Should | Formulario de tasación o contacto para propietarios |
| SEO local | Must | Schema markup (RealEstateAgent, Product), meta tags, sitemap.xml, robots.txt |
| Blog/Artículos | Could | Contenido SEO, artículos del mercado local |
| Testimonios | Could | Reviews de clientes |
| Chat WhatsApp flotante | Should | Botón WhatsApp con prefill mensaje |

### 3.2 Lado admin (dashboard)

| Funcionalidad | Prioridad | Descripción |
|---|---|---|
| Login/Logout | Must | Email + contraseña, 2FA opcional |
| Dashboard principal | Must | KPIs: inmuebles activos, vistas, leads, ratio conversión |
| CRUD completo inmuebles | Must | Crear, editar, eliminar, duplicar inmueble |
| Gestión de imágenes | Must | Upload múltiple, drag & drop, reorder, eliminar, marcar como principal |
| Publicar/despublicar | Must | Toggle visibilidad público/admin |
| Gestión de contactos/leads | Must | Ver inbound queries, asignar agente, marcar como atendidas |
| Feed de portales | Should | Publicar automáticamente en Idealista/Fotocasa vía API |
| Estadísticas | Should | Google Analytics 4 / Plausible integrado |
| Notificaciones interno | Should | Toast cuando llega un lead nuevo |
| Multi-agente | Could | Varios usuarios admin con roles |

### 3.3 Diferencia cliente vs admin

| Vista | Cliente (público) | Admin |
|-------|-------------------|-------|
| Listado | Solo inmuebles publicados | Todos (incluidos no publicados) |
| Detalle | Completo + contacto | Completo + editar |
| Formularios | Solo contacto | CRUD completo |
| Mapas | Sí | Sí (con gestión de marcadores) |
| Dashboard | No | Sí |
| Feed portales | No | Sí |
| Estadísticas | No | Sí |

---

## 4. STACK TECNOLÓGICO

### 4.1 Stack recomendado (full Next.js + Supabase)

**¿Por qué este stack?**
- Next.js 14 App Router: SSR/SSG/ISR nativas → SEO excelente
- Supabase: PostgreSQL + Auth + Storage + Realtime en un solo servicio → reduce complejidad y coste
- Tailwind CSS: desarrollo rápido, responsive painless
- Leaflet: mapas gratis con OSM
- Resend: email transaccional barato (100 emails/día gratis)
- Vercel: hosting Next.js con ISR y edge functions incluidas en el tier gratuito

| Capa | Tecnología | Justificación |
|------|-----------|----------------|
| **Frontend** | Next.js 14 (App Router) | SSR/SSG/ISR, React, buen SEO, código abierto |
| **Estilos** | Tailwind CSS 3 | Rápido, consistente, mobile-first |
| **UI Components** | shadcn/ui | Componentes accesibles, copy-paste, no bloqueado por librería |
| **Base de datos** | PostgreSQL (Supabase) | Relacional, robusto, JSONB para datos flexibles |
| **Auth** | Supabase Auth / NextAuth.js | JWT, providers, session management |
| **Storage** | Supabase Storage | Fotos/vídeos, CDN incluido |
| **Mapas** | Leaflet + React-Leaflet (OSM) | Gratis, sin API key obligatoria |
| **Forms** | React Hook Form + Zod | Validación tipada, performance |
| **Email** | Resend | 100 emails/día gratis, integración React Email |
| **Hosting** | Vercel (o Railway) | CDN global, ISR, deploy automático desde Git |
| **Búsqueda** | Supabase Full Text Search o Meilisearch | Búsqueda de texto completo con typo-tolerance |
| **Gestión de estado** | Zustand o React Query (TanStack Query) | Cacheo, sincronización estado servidor |
| **Testing** | Vitest + Playwright | Unit tests + E2E |
| **Linting** | ESLint + Prettier | Consistencia código |

### 4.2 Alternativas por preferencia

| Necesidad | Opción A | Opción B | Opción C |
|-----------|----------|----------|----------|
| CMS completo | Strapi + Next.js | WordPress headless | Directus + Next.js |
| Más control backend | NestJS + Prisma | Django + DRF | Laravel + Filament |
| Sin backend propio | Supabase | Firebase | PocketBase |
| Mapas premium | Mapbox GL JS | Google Maps Platform | — (usar OSM) |

### 4.3 Lenguaje

**TypeScript** en todo el proyecto (frontend y backend). Justificación: tipado estático reduce bugs, mejor DX, autocompletado.

---

## 5. BASE DE DATOS

### 5.1 Esquema de tablas (PostgreSQL)

```sql
-- ============================================
-- INMUEBLES
-- ============================================
CREATE TABLE properties (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  reference       VARCHAR(50) UNIQUE NOT NULL,  -- ej: "P-2025-0042"
  title           VARCHAR(255) NOT NULL,
  description     TEXT,
  operation       VARCHAR(20) NOT NULL,  -- 'sale' | 'rent' | 'both'
  property_type   VARCHAR(50) NOT NULL,   -- 'flat' | 'house' | 'penthouse' | 'chalet' | 'land' | 'commercial' | 'office' | 'garage'
  status          VARCHAR(20) DEFAULT 'draft',  -- 'draft' | 'published' | 'reserved' | 'sold' | 'rented'
  
  -- Localización
  address         VARCHAR(255),
  city            VARCHAR(100) NOT NULL,
  province        VARCHAR(100) NOT NULL,
  postal_code     VARCHAR(10),
  lat             DECIMAL(10, 8),
  lng             DECIMAL(11, 8),
  
  -- Características
  price           DECIMAL(12, 2) NOT NULL,
  community_fees   DECIMAL(10, 2),   -- gastos comunidad (€/mes)
  m2_built        DECIMAL(8, 2),    -- m² construidos
  m2_useful        DECIMAL(8, 2),    -- m² útiles
  m2_plot         DECIMAL(10, 2),   -- m² parcela (chalets)
  rooms            INTEGER,
  bathrooms        INTEGER,
  half_bathrooms   INTEGER DEFAULT 0,
  floors           INTEGER DEFAULT 1,
  
  -- Detalles adicionales (JSONB para flexibilidad)
  features        JSONB DEFAULT '[]',  -- ['parking', 'pool', 'garden', 'lift', 'terrace'...]
  orientation      VARCHAR(50),        -- 'north' | 'south' | 'east' | 'west'
  floor_number     INTEGER,
  year_built       INTEGER,
  energy_cert      VARCHAR(5),         -- 'A', 'B', 'C', 'D', 'E', 'F', 'G'
  energy_emissions VARCHAR(5),
  
  -- Multimedia
  video_url        VARCHAR(500),        -- YouTube/Vimeo URL
  
  -- SEO
  slug             VARCHAR(255) UNIQUE,
  meta_title        VARCHAR(255),
  meta_description  VARCHAR(500),
  
  -- Metadatos
  published_at     TIMESTAMPTZ,
  created_at       TIMESTAMPTZ DEFAULT NOW(),
  updated_at       TIMESTAMPTZ DEFAULT NOW(),
  created_by       UUID REFERENCES auth.users(id),
  views            INTEGER DEFAULT 0
);

-- ============================================
-- IMÁGENES
-- ============================================
CREATE TABLE property_images (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  property_id UUID NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
  url         VARCHAR(500) NOT NULL,
  public_url  VARCHAR(500),  -- URL pública en CDN
  filename    VARCHAR(255),
  size_bytes  INTEGER,
  mime_type   VARCHAR(100),
  width       INTEGER,
  height      INTEGER,
  alt_text    VARCHAR(255),
  sort_order  INTEGER DEFAULT 0,
  is_primary  BOOLEAN DEFAULT FALSE,
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- CONTACTOS / LEADS
-- ============================================
CREATE TABLE contacts (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  property_id     UUID REFERENCES properties(id),  -- NULL si consulta general
  name            VARCHAR(255) NOT NULL,
  email           VARCHAR(255) NOT NULL,
  phone           VARCHAR(50),
  message         TEXT,
  query_type      VARCHAR(50),  -- 'info' | 'visit' | 'offer' | 'sell' | 'general'
  source          VARCHAR(50),  -- 'web' | 'phone' | 'idealista' | 'fotocasa'
  status          VARCHAR(20) DEFAULT 'new',  -- 'new' | 'contacted' | 'qualified' | 'closed'
  assigned_to     UUID REFERENCES auth.users(id),
  notes           TEXT,
  gdpr_consent    BOOLEAN DEFAULT FALSE,
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- ALERTAS DE BÚSQUEDA
-- ============================================
CREATE TABLE search_alerts (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     UUID REFERENCES auth.users(id),
  email       VARCHAR(255) NOT NULL,
  filters     JSONB NOT NULL,  -- criterios guardados
  frequency   VARCHAR(20) DEFAULT 'daily',  -- 'realtime' | 'daily' | 'weekly'
  is_active   BOOLEAN DEFAULT TRUE,
  last_sent   TIMESTAMPTZ,
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- USUARIOS ADMIN
-- ============================================
CREATE TABLE admin_users (
  id          UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  full_name   VARCHAR(255),
  role        VARCHAR(20) DEFAULT 'agent',  -- 'superadmin' | 'admin' | 'agent'
  phone       VARCHAR(50),
  avatar_url  VARCHAR(500),
  is_active   BOOLEAN DEFAULT TRUE,
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- LOGS DE ACTIVIDAD (audit trail)
-- ============================================
CREATE TABLE activity_log (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     UUID REFERENCES auth.users(id),
  action      VARCHAR(50) NOT NULL,  -- 'create' | 'update' | 'delete' | 'publish' | 'unpublish'
  entity_type VARCHAR(50) NOT NULL,  -- 'property' | 'contact' | 'user'
  entity_id   UUID,
  diff        JSONB,  -- cambios realizados
  ip_address  INET,
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- ÍNDICES
-- ============================================
CREATE INDEX idx_properties_city ON properties(city);
CREATE INDEX idx_properties_operation ON properties(operation);
CREATE INDEX idx_properties_status ON properties(status);
CREATE INDEX idx_properties_price ON properties(price);
CREATE INDEX idx_properties_created ON properties(created_at DESC);
CREATE INDEX idx_properties_slug ON properties(slug);
CREATE INDEX idx_images_property ON property_images(property_id);
CREATE INDEX idx_contacts_property ON contacts(property_id);
CREATE INDEX idx_contacts_status ON contacts(status);

-- Búsqueda texto completo
CREATE INDEX idx_properties_search ON properties USING GIN (
  to_tsvector('spanish', title || ' ' || COALESCE(description, '') || ' ' || city)
);
```

### 5.2 Modelos Prisma correspondientes

```prisma
// schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")
}

model Property {
  id             String    @id @default(uuid())
  reference      String    @unique
  title          String
  description    String?
  operation      String    // sale | rent | both
  propertyType   String    // flat | house | penthouse | chalet | land | commercial | office | garage
  status         String    @default("draft") // draft | published | reserved | sold | rented
  
  address        String?
  city           String
  province       String
  postalCode     String?
  lat            Float?
  lng            Float?
  
  price          Float
  communityFees  Float?
  m2Built        Float?
  m2Useful       Float?
  m2Plot         Float?
  rooms          Int?
  bathrooms      Int?
  halfBathrooms  Int       @default(0)
  floors         Int       @default(1)
  
  features       Json      @default("[]")
  orientation    String?
  floorNumber    Int?
  yearBuilt      Int?
  energyCert     String?
  energyEmissions String?
  
  videoUrl       String?
  
  slug           String?   @unique
  metaTitle      String?
  metaDescription String?
  
  publishedAt    DateTime?
  createdAt      DateTime  @default(now())
  updatedAt      DateTime  @updatedAt
  views          Int       @default(0)
  
  images         PropertyImage[]
  contacts       Contact[]
  
  @@index([city])
  @@index([operation])
  @@index([status])
  @@index([price])
}

model PropertyImage {
  id         String   @id @default(uuid())
  propertyId String
  property   Property @relation(fields: [propertyId], references: [id], onDelete: Cascade)
  url        String
  publicUrl  String?
  filename   String?
  sizeBytes  Int?
  mimeType   String?
  width      Int?
  height     Int?
  altText    String?
  sortOrder  Int       @default(0)
  isPrimary  Boolean  @default(false)
  createdAt  DateTime @default(now())
  
  @@index([propertyId])
}

model Contact {
  id           String    @id @default(uuid())
  propertyId   String?
  property     Property? @relation(fields: [propertyId], references: [id])
  name         String
  email        String
  phone        String?
  message      String?
  queryType    String?
  source       String?
  status       String    @default("new")
  assignedTo   String?
  notes        String?
  gdprConsent  Boolean   @default(false)
  createdAt    DateTime  @default(now())
  updatedAt    DateTime  @updatedAt
  
  @@index([propertyId])
  @@index([status])
}

model SearchAlert {
  id        String   @id @default(uuid())
  userId    String?
  email     String
  filters   Json
  frequency String   @default("daily")
  isActive  Boolean  @default(true)
  lastSent  DateTime?
  createdAt DateTime @default(now())
}

model AdminUser {
  id        String   @id @default(uuid())
  fullName  String?
  role      String   @default("agent")
  phone     String?
  avatarUrl String?
  isActive  Boolean  @default(true)
  createdAt DateTime @default(now())
}
```

---

## 6. INTEGRACIONES CON PORTALES

### 6.1 Idealista

**Web:** developers.idealista.com

| Aspecto | Detalle |
|---------|---------|
| **Qué ofrece** | API REST para publicar/listar inmuebles, búsqueda, detalle de propiedades |
| **Coste** | No es público openly — requiere contactar con comercial. Estimado: desde ~€100-300/mes según volumen. Hay plan "Exporta" para publicar en portal |
| **Requisitos** | Ser profesional inmobiliario con licencia, cuenta Idealista Premium/Pro activa |
| **Autenticación** | API Key + Secret (OAuth 2.0 client credentials) |
| **Formato** | JSON REST |
| **Límites** | Rate limiting por plan |
| **Feed disponible** | Sí, feed de publicación + consulta |
| **Notas** | El plan "Exporta" permite publicar en Idealista y sus portales asociados (Facilita, etc.) |

**Coste estimado real:** Si ya tienes cuenta Pro (€XX/mes), la API suele venir incluida. Coste adicional estimado: €0-200/mes dependiendo del planchosen.

### 6.2 Fotocasa

| Aspecto | Detalle |
|---------|---------|
| **Qué ofrece** | API para publicación de anuncios, consulta de listado |
| **Coste** | Requiere cuenta profesional. Contactar con comercial. Estimado: €100-250/mes |
| **Requisitos** | Ser agente inmobiliario registrado |
| **Autenticación** | API Key |
| **Formato** | JSON REST |
| **Notas** | Pertenece al grupo Adevinta (igual que Habitaclia). Reutiliza mucho de su infraestructura |

### 6.3 Kyero

| Aspecto | Detalle |
|---------|---------|
| **Qué ofrece** | Feed XML/CSV para publicar propiedades orientadas a mercado internacional (británicos, nórdicos, holandeses) |
| **Coste** | Gratis para agencias que cumplan sus requisitos de calidad |
| **Formato** | XML (formato Kyero XML v3.0) |
| **Requisitos** | Feed con datos estructurados, imágenes con URLs públicas |
| **Notas** | Muy útil para inmobiliaria local con propiedades de interés para extranjeros en zonas costeras |

### 6.4 Rightmove (para mercado internacional)

| Aspecto | Detalle |
|---------|---------|
| **Qué ofrece** | Portal inmobiliario UK nº1. Feed para publicar propiedades españolas para compradores británicos |
| **Coste** | Fee de listado + suscripción mensual. Desde £99/mes aproximadamente |
| **Formato** | Rightmove XML feed |
| **Notas** | Requiere cuenta de agente UK. Útil en zonas costeras/balnearias con demanda británica |

### 6.5 Alternatives gratuitas

| Portal | Coste | Formato | Notas |
|--------|-------|---------|-------|
| **Enalquiler** | Gratis | Web manual / CSV | Portal español de alquiler |
| **Nesting** | Gratis (básico) | Web | Enfocado alquiler |
| **FaceIt** | Gratis | Web | Alternativa indie |
| **TuHabitissimo** | Fee por lead | Web | Especializado en reformas/post-venta |
| **Infojobs / Jobandtalent casas** | N/A | — | No aplica |

### 6.6 Comparativa de esfuerzo de integración

| Portal | Dificultad | Coste real | Esfuerzo dev |
|--------|-----------|------------|--------------|
| Idealista | Alta | €€€ | Alto (OAuth, rate limits, spec compleja) |
| Fotocasa | Alta | €€ | Alto (similar a Idealista) |
| Kyero | Baja | € | Bajo (feed XML, formato simple) |
| Rightmove | Media | ££ | Medio (spec UK) |
| Enalquiler | Baja | € | Bajo (manual o CSV) |

**Recomendación:** Empezar con **Kyero** (gratis, fácil, alcance internacional) + publicar manualmente en Idealista si el presupuesto lo permite. Idealista y Fotocasa son las优先级 más altas para el mercado español.

---

## 7. COSTE ESTIMADO

### 7.1 Costes mensuales (producción)

| Servicio | Opción | Coste/mes | Notas |
|----------|--------|-----------|-------|
| Hosting frontend | Vercel Pro | €0-20 | Gratis tier: 100GB bandwidth, 100 serverless functions |
| Base de datos + Auth + Storage | Supabase Pro | €0-25 | Gratis tier: 500MB DB, 1GB storage, 50k auth users |
| Dominio | Namecheap / Cloudflare Registrar | €8-12/año | ~€1/mes |
| SSL | Incluido en hosting | €0 | Let's Encrypt (gratis) |
| Email transaccional | Resend Free | €0 | 100 emails/día |
| Mapa | Leaflet + OSM | €0 | Sin API key |
| Mapa premium | Mapbox | €0-50 | Solo si necesitas estilo premium |
| Email corporativo | Google Workspace o Microsoft 365 | €6-12 | 1 usuario mínimo para empezar |
| Analytics | Plausible | €0-9 | Gratis tier: 10k pageviews/mes |

**Total mes (arranque):** €0-50/mes
**Total mes (crecimiento):** €50-150/mes

### 7.2 Costes de desarrollo (si se terceariza)

| Fase | Estimación horas | Coste orientativo |
|------|-----------------|-------------------|
| Diseño UX/UI + branding | 20-40h | €1.000-3.000 |
| Setup proyecto + infraestructura | 8-16h | €400-1.000 |
| Frontend público (home, listado, detalle) | 40-80h | €2.000-5.000 |
| Dashboard admin + CRUD | 40-80h | €2.000-5.000 |
| Integraciones (mapas, email, portales) | 16-32h | €800-2.000 |
| SEO + legal (RGPD, cookies) | 8-16h | €400-1.000 |
| Testing + deploy | 8-16h | €400-1.000 |
| **Total** | **140-280h** | **€7.000-18.000** |

> **Nota:** Esto es para desarrollo a medida con Next.js + Supabase. Un enfoque con WordPress + plugin (Flatsome + Houzez/Realty) reduciría coste pero limitaría flexibilidad y escalabilidad.

### 7.3 Costes recurrentes anuales

| Concepto | Coste/año |
|----------|-----------|
| Dominio | €10-15 |
| Hosting | €0-240 |
| Supabase | €0-300 |
| Email corporativo | €72-144 |
| Idealista API (si aplica) | €1.200-3.600 |
| Fotocasa API (si aplica) | €1.200-3.000 |
| **Total sin portales** | **~€400-700/año** |
| **Total con portales** | **~€3.000-7.000/año** |

---

## 8. FASES DE DESARROLLO

### Fase 0 — Fundamentos (Semana 1-2)
1. Registrar dominio
2. Crear cuenta Vercel + Supabase
3. Inicializar proyecto Next.js 14 con TypeScript
4. Configurar Tailwind CSS + shadcn/ui
5. Configurar Supabase (DB, Auth, Storage)
6. Ejecutar migración Prisma
7. Setup ESLint + Prettier + Husky
8. Deploy inicial (preview)

**Entregable:** Proyecto base deployado.

### Fase 1 — Frontend público mínimo (Semana 2-4)
1. Header + Footer
2. Página home con hero + buscador
3. Página listado con filtros
4. Página detalle inmueble (SSR)
5. Galería de fotos (lightbox)
6. Mapa con Leaflet
7. Formulario de contacto
8. Responsive completo

**Entregable:** Web pública usable sin backend admin.

### Fase 2 — Backend + CMS admin (Semana 4-7)
1. Dashboard admin con autenticación
2. CRUD completo de inmuebles
3. Upload de imágenes con reorder
4. Gestión de contacts/leads
5. Publicar/despublicar toggle
6. Vista de estadísticas básicas

**Entregable:** Inmobiliaria puede gestionar su catálogo.

### Fase 3 — SEO + Legal (Semana 6-8)
1. Schema markup (RealEstateAgent + Product)
2. Sitemap.xml dinámico
3. robots.txt
4. Meta tags dinámicos por inmueble
5. Política de privacidad
6. Aviso legal
7. Política de cookies (consentimiento)
8. RGPD: checkbox en formularios, derecho de oposición

**Entregable:** Web compliant con normativa española.

### Fase 4 — Integraciones (Semana 7-10)
1. Email transaccional (Resend)
2. Alerts de búsqueda (email periódico)
3. Integración con Google Analytics 4 / Plausible
4. Feed XML para Kyero
5. Publicación manual en Idealista (si cuenta Pro)

**Entregable:** Web completa con integraciones.

### Fase 5 — Extras y optimización (Semana 10-12)
1. Performance: Core Web Vitals, imagen optimization (Next/Image)
2. Mobile: PWA, standalone manifest
3. Chat WhatsApp flotante
4. Multi-idioma (si zona con demanda internacional)
5. Blog básico (Next.js + MDX)
6. Testing E2E (Playwright)

**Entregable:** Producto pulido y listo para producción real.

---

## 9. REQUISITOS LEGALES Y TÉCNICOS (España)

### 9.1 RGPD (Reglamento General de Protección de Datos)

- **Base legal:** Consentimiento explícito para tratamiento de datos personales.
- **Forms:** Incluir checkbox obligatorio: "Acepto la política de privacidad" con enlace.
- **Derechos:** Implementar mecanismo para ejercicio de derechos (acceso, rectificación, supresión, portabilidad).
- **Delegado:** Para inmobiliaria pequeña (datos limitados), no es obligatorio DPO.
- **Registro de actividad:** Mantener log de tratamientos.
- **Brechas:** Plan de notificación a autoridad (AEPD) en 72h.
- **Nota:** Esto no es asesoramiento legal. Consultar con un abogado para caso específico.

### 9.2 Ley de Servicios de la Sociedad de la Información (LSSI)

- **Identificación:** Razón social, CIF, domicilio, email de contacto visibles en footer.
- **Inscripción registral:** Si aplica (Registro Mercantil).
- **Precios:** Indicar si incluyen o no impuestos (IVA).
- **Código de conducta:** Opcional pero recomendado.

### 9.3 Ley de Propiedad Horizontal + Ley de Arrendamientos Urbanos

- Para **alquileres**: información obligatoria en contrato y en algunos casos en el anuncio (ver RD 233/2013 y LAU).
- EPC (Certificado de Eficiencia Energética): obligatorio indicar en anuncio (clasificación energética A-G).
- Información de gastos de comunidad, IBI, depósitos legales.

### 9.4 Cookies

- Banner de cookies al entrar (cookie consent).
- Opciones: aceptar / rechazar / configurar.
- Preferencias guardadas.
- Herramientas: Cookiebot, OneTrust, o cookieyes