# TECNICAS.md — Apuntes técnicos detallados

> Dependencias, comandos de setup, estructura de carpetas, consideraciones de deployment y anything que un developer necesita para ponerse a construir.

---

## 1. INICIALIZACIÓN DEL PROYECTO

### 1.1 Crear proyecto Next.js 14

```bash
# Con create-next-app (App Router, TypeScript, Tailwind)
npx create-next-app@latest inmobiliaria-web \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --src-dir \
  --import-alias "@/*" \
  --no-turbopack

cd inmobiliaria-web
```

### 1.2 Instalar dependencias principales

```bash
# ─── Core ───────────────────────────────────────────
npm install next@14 react react-dom

# ─── UI / Estilos ──────────────────────────────────
npm install -D tailwindcss postcss autoprefixer
npm install @tailwindcss/typography  # Para prose de descripciones
npm install shadcn-ui   # Luego: npx shadcn-ui@latest init

# ─── Base de datos ──────────────────────────────────
npm install prisma @prisma/client

# ─── Mapas ─────────────────────────────────────────
npm install leaflet react-leaflet
npm install -D @types/leaflet

# ─── Forms ─────────────────────────────────────────
npm install react-hook-form @hookform/resolvers zod

# ─── Gestión de estado / data fetching ──────────────
npm install @tanstack/react-query
npm install zustand  # Estado global simple

# ─── Email ──────────────────────────────────────────
npm install resend @react-email/components

# ─── Mapas premium (opcional) ──────────────────────
npm install mapbox-gl react-mapbox-gl

# ─── Imágenes / Upload ──────────────────────────────
npm install react-dropzone

# ─── Utilidades ─────────────────────────────────────
npm install clsx tailwind-merge
npm install date-fns
npm install slugify

# ─── Testing ────────────────────────────────────────
npm install -D vitest @vitejs/plugin-react
npm install -D @playwright/test
npx playwright install --with-deps chromium

# ─── Linting ─────────────────────────────────────────
npm install -D eslint prettier
npm install -D eslint-config-next
npm install -D lint-staged husky
```

### 1.3 Setup shadcn/ui

```bash
npx shadcn-ui@latest init
# Config:
# Style: Default
# Base color: Slate
# CSS variables: Yes
# → Añadir componentes según necesidad:
npx shadcn-ui@latest add button card badge input label textarea
npx shadcn-ui@latest add dialog sheet dropdown-menu tabs toast
npx shadcn-ui@latest add table form select checkbox slider
```

### 1.4 Setup Prisma + Supabase

```bash
# Inicializar Prisma
npx prisma init

# Configurar .env
cat >> .env << 'EOF'
DATABASE_URL="postgresql://postgres:[PASSWORD]@db.[PROJECT_ID].supabase.co:5432/postgres"
DIRECT_URL="postgresql://postgres:[PASSWORD]@db.[PROJECT_ID].supabase.co:5432/postgres"
NEXT_PUBLIC_SUPABASE_URL="https://[PROJECT_ID].supabase.co"
NEXT_PUBLIC_SUPABASE_ANON_KEY="eyJhbGc..."
SUPABASE_SERVICE_ROLE_KEY="eyJhbGc..."
RESEND_API_KEY="re_xxxxx"
NEXT_PUBLIC_APP_URL="http://localhost:3000"
NEXT_PUBLIC_APP_URL_PROD="https://midominio.es"
EOF

# Generar cliente Prisma
npx prisma generate

# Crear tablas en Supabase
npx prisma db push   # Push schema a Supabase

# Ver schema en Prisma Studio
npx prisma studio    # http://localhost:5555
```

---

## 2. ESTRUCTURA DE CARPETAS

```
inmobiliaria-web/
├── prisma/
│   ├── schema.prisma          # Definición de modelos
│   └── migrations/            # Migraciones (generadas)
│
├── public/
│   ├── images/
│   │   ├── logo.svg
│   │   ├── og-image.jpg       # Open Graph image
│   │   └── placeholder.svg    # Imagen placeholder
│   ├── robots.txt
│   ├── sitemap.xml            # Generado dinámicamente
│   └── favicon.ico
│
├── src/
│   │
│   ├── app/                   # Next.js App Router
│   │   ├── (public)/          # Grupo de rutas públicas
│   │   │   ├── page.tsx               # Home
│   │   │   ├── layout.tsx            # Header + Footer público
│   │   │   ├── contacto/
│   │   │   │   └── page.tsx
│   │   │   ├── inmuebles/
│   │   │   │   ├── page.tsx           # Listado
│   │   │   │   └── [slug]/
│   │   │   │       └── page.tsx       # Detalle
│   │   │   └── Politik/
│   │   │       ├── privacidad/
│   │   │       │   └── page.tsx
│   │   │       ├── cookies/
│   │   │       │   └── page.tsx
│   │   │       └── aviso-legal/
│   │   │           └── page.tsx
│   │   │
│   │   ├── (admin)/           # Grupo rutas admin (con auth)
│   │   │   ├── (dashboard)/
│   │   │   │   ├── layout.tsx         # Admin layout con sidebar
│   │   │   │   ├── page.tsx           # Dashboard
│   │   │   │   ├── propiedades/
│   │   │   │   │   ├── page.tsx       # Listado admin
│   │   │   │   │   ├── nuevo/
│   │   │   │   │   │   └── page.tsx
│   │   │   │   │   └── [id]/
│   │   │   │   │       └── editar/
│   │   │   │   │           └── page.tsx
│   │   │   │   ├── leads/
│   │   │   │   │   └── page.tsx
│   │   │   │   └── ajustes/
│   │   │   │       └── page.tsx
│   │   │   └── login/
│   │   │       └── page.tsx
│   │   │
│   │   ├── api/               # API Routes
│   │   │   ├── propiedades/
│   │   │   │   ├── route.ts          # GET (listado), POST (crear)
│   │   │   │   └── [id]/
│   │   │   │       └── route.ts      # GET, PUT, DELETE
│   │   │   ├── contacts/
│   │   │   │   └── route.ts
│   │   │   ├── leads/
│   │   │   │   └── route.ts
│   │   │   ├── upload/
│   │   │   │   └── route.ts
│   │   │   ├── search/
│   │   │   │   └── route.ts
│   │   │   └── sitemap/
│   │   │       └── route.ts
│   │   │
│   │   ├── layout.tsx         # Root layout
│   │   ├── globals.css
│   │   └── not-found.tsx
│   │
│   ├── components/
│   │   ├── ui/                # shadcn/ui componentes base
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── badge.tsx
│   │   │   └── ...
│   │   │
│   │   ├── layout/            # Componentes de layout
│   │   │   ├── header/
│   │   │   │   ├── header.tsx
│   │   │   │   └── header.module.css
│   │   │   ├── footer/
│   │   │   │   └── footer.tsx
│   │   │   └── admin-sidebar/
│   │   │       └── sidebar.tsx
│   │   │
│   │   ├── properties/        # Componentes específicos de inmuebles
│   │   │   ├── property-card.tsx
│   │   │   ├── property-gallery.tsx
│   │   │   ├── property-filters.tsx
│   │   │   ├── property-map.tsx
│   │   │   ├── property-table.tsx   # Admin
│   │   │   └── property-form.tsx
│   │   │
│   │   ├── forms/
│   │   │   ├── contact-form.tsx
│   │   │   ├── search-form.tsx
│   │   │   └── login-form.tsx
│   │   │
│   │   └── shared/
│   │       ├── image-upload.tsx
│   │       ├── map-picker.tsx
│   │       ├── price-display.tsx
│   │       └── schema-markup.tsx
│   │
│   ├── lib/
│   │   ├── db.ts              # Cliente Prisma singleton
│   │   ├── supabase.ts        # Cliente Supabase
│   │   ├── auth.ts            # Utils de autenticación
│   │   ├── email.ts           # Config Resend
│   │   ├── validators.ts      # Zod schemas compartidos
│   │   ├── utils.ts           # cn(), formatPrice(), etc.
│   │   └── constants.ts        # Tipos de inmueble, operaciones, etc.
│   │
│   ├── types/
│   │   ├── property.ts        # Tipos para Property
│   │   ├── contact.ts
│   │   └── admin.ts
│   │
│   ├── hooks/
│   │   ├── use-properties.ts  # React Query hooks
│   │   ├── use-contacts.ts
│   │   ├── use-auth.ts
│   │   └── use-map.ts
│   │
│   └── emails/                 # React Email templates
│       ├── contact-notification.tsx
│       ├── lead-notification.tsx
│       └── search-alert.tsx
│
├── .env.local                  # Variables locales (NO commitear)
├── .env.example                # Template de .env
├── .gitignore
├── .prettierrc
├── .eslintrc.json
├── next.config.ts              # Config Next.js
├── tailwind.config.ts
├── tsconfig.json
├── vitest.config.ts
└── package.json
```

---

## 3. CONFIGURACIONES CLAVE

### 3.1 next.config.ts

```ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '*.supabase.co',
      },
      {
        protocol: 'https',
        hostname: '*.public.vm.supabase.co',
      },
      {
        protocol: 'https',
        hostname: 'images.unsplash.com',
      },
    ],
  },
  // ISR: revalidate cada hora para listados
  experimental: {
    // Para Next.js 14: partial prerender (opcional)
  },
}

export default nextConfig
```

### 3.2 tailwind.config.ts

```ts
import type { Config } from 'tailwindcss'

const config: Config = {
  darkMode: ['class'],
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          primary: '#1B3A5C',
          secondary: '#C9A84C',
          surface: '#F2F2F0',
          background: '#FAFAF8',
          text: '#2D2D2D',
          muted: '#6B7280',
        },
      },
      fontFamily: {
        display: ['var(--font-playfair)', 'Georgia', 'serif'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('tailwindcss-animate'),  // npm install -D tailwindcss-animate
  ],
}

export default config
```

### 3.3 .env.example

```bash
# DATABASE
DATABASE_URL="postgresql://postgres:[PASSWORD]@db.[ID].supabase.co:5432/postgres"
DIRECT_URL="postgresql://postgres:[PASSWORD]@db.[ID].supabase.co:5432/postgres"

# SUPABASE
NEXT_PUBLIC_SUPABASE_URL="https://[ID].supabase.co"
NEXT_PUBLIC_SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
SUPABASE_SERVICE_ROLE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# AUTH (NextAuth o Supabase Auth)
NEXTAUTH_URL="http://localhost:3000"
NEXTAUTH_SECRET="[generar con: openssl rand -base64 32]"

# EMAIL
RESEND_API_KEY="re_xxxxx"
EMAIL_FROM="Inmobiliaria <noreply@midominio.es>"

# MAPS
NEXT_PUBLIC_MAPBOX_TOKEN="pk.xxx"  # Opcional, solo si Mapbox

# APP
NEXT_PUBLIC_APP_URL="http://localhost:3000"
NEXT_PUBLIC_APP_URL_PROD="https://midominio.es"
```

---

## 4. COMANDOS DE DESARROLLO

```bash
# ─── Instalación ──────────────────────────────────
npm install
npx prisma generate          # Generar tipos Prisma
npx prisma db push           # Crear tablas en DB
# Crear cuenta Supabase y copiar credentials

# ─── Desarrollo ───────────────────────────────────
npm run dev                   # http://localhost:3000
npx prisma studio             # Admin DB visual (puerto 5555)

# ─── Testing ──────────────────────────────────────
npm run test                  # Vitest unit tests
npx playwright test           # E2E tests
npx playwright test --ui      # E2E con UI

# ─── Build ────────────────────────────────────────
npm run build                 # Build producción
npm run start                 # Servir build localmente

# ─── Linting ──────────────────────────────────────
npm run lint                  # ESLint
npm run format                # Prettier

# ─── Deployment ────────────────────────────────────
# Vercel (recomendado):
vercel deploy
# o desde GitHub: conectar repo → deploy automático

# Railway:
railway deploy

# ─── Generar secreto ──────────────────────────────
openssl rand -base64 32        # Para NEXTAUTH_SECRET
```

---

## 5. PATRONES DE CÓDIGO FRECUENTES

### 5.1 Server Component con fetch (SSR/ISR)

```tsx
// src/app/inmuebles/page.tsx
import { prisma } from '@/lib/db'

// Ejemplo: ISR (revalidate cada hora)
export const revalidate = 3600

async function getProperties(searchParams: {
  operation?: string
  city?: string
  minPrice?: string
  maxPrice?: string
  page?: string
}) {
  const page = Number(searchParams.page) || 1
  const perPage = 12

  const where = {
    status: 'published',
    ...(searchParams.operation && { operation: searchParams.operation }),
    ...(searchParams.city && { city: { contains: searchParams.city, mode: 'insensitive' as const } }),
    ...(searchParams.minPrice && { price: { gte: Number(searchParams.minPrice) } }),
    ...(searchParams.maxPrice && { price: { lte: Number(searchParams.maxPrice) } }),
  }

  const [properties, total] = await Promise.all([
    prisma.property.findMany({
      where,
      include: { images: { where: { isPrimary: true }, take: 1 } },
      orderBy: { createdAt: 'desc' },
      skip: (page - 1) * perPage,
      take: perPage,
    }),
    prisma.property.count({ where }),
  ])

  return { properties, total, pages: Math.ceil(total / perPage) }
}

export default async function PropertiesPage({
  searchParams,
}: {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>
}) {
  const resolvedParams = await searchParams
  const { properties, total, pages } = await getProperties(resolvedParams)

  return (
    <PropertiesGrid
      properties={properties}
      total={total}
      pages={pages}
      searchParams={resolvedParams}
    />
  )
}
```

### 5.2 Client Component (formulario de contacto)

```tsx
// src/components/forms/contact-form.tsx
'use client'

import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { contactSchema } from '@/lib/validators'

type ContactFormData = z.infer<typeof contactSchema>

export function ContactForm({ propertyId }: { propertyId?: string }) {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm<ContactFormData>({
    resolver: zodResolver(contactSchema),
  })

  async function onSubmit(data: ContactFormData) {
    const res = await fetch('/api/contacts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...data, propertyId }),
    })

    if (!res.ok) throw new Error('Error enviando')
    reset()
    // Toast success
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('name')} placeholder="Nombre" />
      {errors.name && <span>{errors.name.message}</span>}

      <input {...register('email')} type="email" placeholder="Email" />
      {errors.email && <span>{errors.email.message}</span>}

      <textarea {...register('message')} placeholder="Mensaje" />
      {errors.message && <span>{errors.message.message}</span>}

      <label>
        <input type="checkbox" {...register('gdprConsent')} />
        Acepto la política de privacidad
      </label>
      {errors.gdprConsent && <span>{errors.gdprConsent.message}</span>}

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Enviando...' : 'Enviar'}
      </button>
    </form>
  )
}
```

### 5.3 API Route (crear contacto)

```ts
// src/app/api/contacts/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/db'
import { contactSchema } from '@/lib/validators'
import { sendContactEmail } from '@/lib/email'

export async function POST(req: NextRequest) {
  const body = await req.json()

  // Validar con Zod
  const parsed = contactSchema.safeParse(body)
  if (!parsed.success) {
    return NextResponse.json(
      { error: 'Datos inválidos', details: parsed.error.flatten() },
      { status: 400 }
    )
  }

  // Guardar en DB
  const contact = await prisma.contact.create({
    data: {
      name: parsed.data.name,
      email: parsed.data.email,
      phone: parsed.data.phone,
      message: parsed.data.message,
      queryType: parsed.data.queryType,
      propertyId: parsed.data.propertyId,
      gdprConsent: parsed.data.gdprConsent,
      source: 'web',
    },
  })

  // Enviar email de notificación
  await sendContactEmail(contact)

  // Realtime notification (Supabase)
  // await supabase.channel('admin-notifications').send({ type: 'broadcast', event: 'new_lead', payload: contact })

  return NextResponse.json({ success: true, id: contact.id }, { status: 201 })
}
```

### 5.4 Utility: cn() para clases

```ts
// src/lib/utils.ts
import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

### 5.5 Image upload (Supabase Storage)

```ts
// src/app/api/upload/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { createClient } from '@supabase/supabase-js'

const supabaseAdmin = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
)

export async function POST(req: NextRequest) {
  const formData = await req.formData()
  const file = formData.get('file') as File
  const propertyId = formData.get('propertyId') as string

  if (!file || !propertyId) {
    return NextResponse.json({ error: 'Faltan datos' }, { status: 400 })
  }

  const ext = file.name.split('.').pop()
  const filename = `${propertyId}/${Date.now()}.${ext}`

  const { data, error } = await supabaseAdmin.storage
    .from('property-images')
    .upload(filename, file, {
      cacheControl: '3600',
      upsert: false,
    })

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }

  // Obtener URL pública
  const { data: urlData } = supabaseAdmin.storage
    .from('property-images')
    .getPublicUrl(data.path)

  return NextResponse.json({ url: urlData.publicUrl, path: data.path })
}
```

---

## 6. MIDDLEWARE (protección rutas admin)

```ts
// src/middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { createClient } from '@supabase/supabase-js'

export async function middleware(req: NextRequest) {
  const { pathname } = req.nextUrl

  // Proteger rutas /admin (excepto /admin/login)
  if (pathname.startsWith('/admin') && !pathname.startsWith('/admin/login')) {
    const supabase = createClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
    )

    const { data: { user }, error } = await supabase.auth.getUser()

    if (!user) {
      const loginUrl = new URL('/admin/login', req.url)
      loginUrl.searchParams.set('redirect', pathname)
      return NextResponse.redirect(loginUrl)
    }
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/admin/:path*'],
}
```

---

## 7. SITEMAP DINÁMICO

```ts
// src/app/api/sitemap/route.ts
import { MetadataRoute } from 'next'
import { prisma } from '@/lib/db'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = process.env.NEXT_PUBLIC_APP_URL_PROD!

  // Inmuebles publicados
  const properties = await prisma.property.findMany({
    where: { status: 'published' },
    select: { slug: true, updatedAt: true, publishedAt: true },
  })

  const propertyUrls = properties.map((p) => ({
    url: `${baseUrl}/inmuebles/${p.slug}`,
    lastModified: p.updatedAt || p.publishedAt || new Date(),
    changeFrequency: 'weekly' as const,
    priority: 0.8,
  }))

  // Páginas estáticas
  const staticUrls: MetadataRoute.Sitemap = [
    { url: baseUrl, lastModified: new Date(), changeFrequency: 'daily', priority: 1 },
    { url: `${baseUrl}/inmuebles`, lastModified: new Date(), changeFrequency: 'hourly', priority: 0.9 },
    { url: `${baseUrl}/contacto`, lastModified: new Date(), changeFrequency: 'monthly', priority: 0.5 },
  ]

  return [...staticUrls, ...propertyUrls]
}
```

---

## 8. DEPLOYMENT

### 8.1 Vercel (recomendado)

```bash
# Instalar Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy preview
vercel

# Deploy producción
vercel --prod

# Variables de entorno (desde dashboard Vercel o CLI)
vercel env add DATABASE_URL
vercel env add NEXT_PUBLIC_SUPABASE_URL
vercel env add NEXT_PUBLIC_SUPABASE_ANON_KEY
vercel env add SUPABASE_SERVICE_ROLE_KEY
vercel env add RESEND_API_KEY
vercel env add NEXTAUTH_SECRET
vercel env add NEXTAUTH_URL
```

**Configuración Vercel (vercel.json):**
```json
{
  "framework": "nextjs",
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "X-XSS-Protection", "value": "1; mode=block" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" }
      ]
    }
  ]
}
```

### 8.2 Railway (alternativa)

```bash
# Instalar Railway CLI
npm i -g @railway/cli
railway login

# Iniciar proyecto
railway init
railway add --database postgresql

# Deploy
railway up

# Variables desde .env
railway run npm run build
```

### 8.3 Supabase setup (production)

1. Crear proyecto en [supabase.com](https://supabase.com)
2. Copiar `DATABASE_URL` de Settings → Connection Stringing
3. Ejecutar `npx prisma db push` para crear tablas
4. Crear bucket `property-images` en Storage (público o con RLS)
5. Configurar RLS (Row Level Security) para storage:
   ```sql
   -- Storage: permitir upload si authenticated
   CREATE POLICY "Authenticated upload" ON storage.objects
   FOR INSERT TO authenticated WITH CHECK (bucket_id = 'property-images');
   ```
6. Configurar Auth: Email templates personalizados, disable signup si no quieres registros públicos.

### 8.4 Dominio + SSL

1. Comprar dominio en Namecheap/Cloudflare Registrar (~€10/año)
2. En Vercel: Project → Domains → añadir dominio
3. DNS: añadir registro CNAME apuntando a `cname.vercel-dns.com`
4. SSL: automático (Let's Encrypt via Vercel)
5. Para email: configurar registros MX en DNS (Google Workspace o similar)

### 8.5 Pre requisitos para producción

| Componente | Requisito mínimo |
|-----------|-----------------|
| RAM | 1GB (Vercel: illimité) |
| CPU | Shared (Vercel serverless) |
| DB | PostgreSQL 1GB storage (Supabase free tier) |
| Storage | 1GB imágenes (Supabase free: 1GB) |
| Bandwidth | 100GB/mes (Vercel free tier) |
| Build | <10 min (Vercel timeout) |

---

## 9. TESTING

### 9.1 Unit tests (Vitest)

```bash
npm install -D vitest @vitejs/plugin-react jsdom
```

```ts
// vitest.config.ts
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
  },
})
```

```tsx
// src/lib/__tests__/utils.test.ts
import { describe, it, expect } from 'vitest'
import { formatPrice } from '../utils'

describe('formatPrice', () => {
  it('formatea precio correctamente', () => {
    expect(formatPrice(295000)).toBe('295.000 €')
  })
})
```

### 9.2 E2E Tests (Playwright)

```bash
npx playwright test
```

```ts
// e2e/properties.spec.ts
import { test, expect } from '@playwright/test'

test('listado muestra inmuebles', async ({ page }) => {
  await page.goto('/inmuebles')
  await expect(page.locator('h1')).toContainText('Inmuebles')
  await expect(page.locator('[data-testid="property-card"]').first()).toBeVisible()
})

test('formulario contacto funciona', async ({ page }) => {
  await page.goto('/inmuebles')
  await page.click('[data-testid="contact-button"]')
  await page.fill('[name="name"]', 'Test User')
  await page.fill('[name="email"]', 'test@test.com')
  await page.check('[name="gdprConsent"]')
  await page.click('[type="submit"]')
  await expect(page.locator('[data-testid="success-message"]')).toBeVisible()
})
```

---

## 10. SEGURIDAD

### 10.1 Prácticas obligatorias

- **Nunca** hardcodear secrets: usar variables de entorno
- **RLS en Supabase**: activar Row Level Security en todas las tablas
- **Validación Zod** en TODAS las API routes y forms
- **CSRF**: Next.js API Routes incluyen protección por defecto
- **Rate limiting**: implementar en endpoints públicos (contacts, search)
  ```ts
  // Middleware simple de rate limiting (o usar upstash/ratelimit)
  const rateLimit = { limit: 10, window: '1 minute' }
  ```
- **Upload files**: validar MIME type, tamaño máximo (10MB), extensiones permitidas
- **SQL injection**: Prisma previene por defecto con parameterized queries
- **XSS**: React escapa por defecto; evitar `dangerouslySetInnerHTML` salvo que sea seguro

### 10.2 Checklist pre-lanzamiento

```
☐ Todos los .env en Vercel/Railway configurados
☐ Supabase RLS habilitado y políticas creadas
☐ SSL activo (dominio configurado en Vercel)
☐ Sitemap.xml accesible en /sitemap.xml
☐ robots.txt no bloquea recursos importantes
☐ Meta tags dinámicos en cada página
☐ Schema markup RealEstateAgent en home
☐ Schema markup Product en cada inmueble
☐ Política de privacidad accesible
☐ Política de cookies con consentimiento
☐ Aviso legal con datos de empresa
☐ Formularios con checkbox RGPD
☐ SSL certificate válido (Let's Encrypt)
☐ Imágenes optimizadas (Next/Image con sizes)
☐ Lighthouse performance > 80
☐ Mobile-friendly (Responsive test)
☐ Testing: E2E covers happy paths
☐ Backup de base de datos configurado (Supabase daily backup)
☐ Monitoring: Uptime monitoring (uptimerobot.com gratis)
```

---

## 11. EXTRAS NO TAN OBVIOS

### 11.1 PDF de inmueble

Generar ficha PDF con datos del inmueble para descarga:
```bash
npm install @react-pdf/renderer
```
Template: datos del inmueble → PDF formateado (buena opción para leads que piden información offline).

### 11.2 Open Graph dinámico

```tsx
// src/app/inmuebles/[slug]/opengraph-image.tsx
export function generateOpenGraphImage({ params }: { params: { slug: string } }) {
  return (
    <div style={{ width: 1200, height: 630, background: '#1B3A5C' }}>
      <img src={`${baseUrl}/api/og/${params.slug}`} />
    </div>
  )
}
```

### 11.3 WhatsApp prefill

```tsx
<a
  href={`https://wa.me/34612345678?text=${encodeURIComponent(
    `Hola, me interesa el inmueble ${property.title} (REF: ${property.reference})`
  )}`}
  target="_blank"
  rel="noopener noreferrer"
>
  Escribir por WhatsApp
</a>
```

### 11.4 Calculadora de hipoteca

Integración con API de algún banco o calculadora propia con tipos de interés actuales.

### 11.5 Google Business Profile

Crear y verificar Google Business Profile para la inmobiliaria → aparece en Google Maps y búsqueda local.

### 11.6 Structured Data (Schema.org)

```tsx
// En el head de cada página de detalle
<script
  type="application/ld+json"
  dangerouslySetInnerHTML={{
    __html: JSON.stringify({
      '@context': 'https://schema.org',
      '@type': 'RealEstateListing',
      name: property.title,
      description: property.description,
      url: `${baseUrl}/inmuebles/${property.slug}`,
      image: property.images[0]?.url,
      offers: {
        '@type': 'Offer',
        price: property.price,
        priceCurrency: 'EUR',
        availability: property.status === 'published'
          ? 'https://schema.org/InStock'
          : 'https://schema.org/SoldOut',
      },
      address: {
        '@type': 'PostalAddress',
        streetAddress: property.address,
        addressLocality: property.city,
        postalCode: property.postalCode,
        addressRegion: property.province,
        addressCountry: 'ES',
      },
    }),
  }}
/>
```

### 11.7 Migración desde WordPress (si aplica)

Si hay un WordPress existente:
1. Exportar datos con WP All Export (inmuebles → CSV)
2. Parsear CSV → insertar en Prisma
3. Migrar imágenes a Supabase Storage
4. Redirecciones 301 en `next.config.ts` para mantener SEO de URLs antiguas

---

## 12. HERRAMIENTAS ÚTILES

| Necesidad | Herramienta |
|-----------|------------|
| Diseño UI | Figma (free tier) |
| Mockups | figma.com, wireflow.co |
| Imágenes stock | unsplash.com, pexels.com |
| Iconos | lucide-react, heroicons |
| Animaciones | framer-motion |
| Monitoreo uptime | uptimerobot.com (gratis) |
| Analytics | Plausible (€9/mes, privacy-first) o GA4 (gratis) |
| Error tracking | Sentry (free tier: 5k events/mo) |
| CMDB | Supabase Dashboard |
| Logs | Vercel Analytics |
| CDN images | Next.js Image (automatico con Vercel) |
| Email transactional | Resend |
| Email marketing (newsletter) | Mailchimp (free: 500 contacts) |
