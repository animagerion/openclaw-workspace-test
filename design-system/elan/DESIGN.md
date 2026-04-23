---
version: alpha
name: Élan Forensic
description: Corporate legal and forensic consultancy brand. Warm palette (red/orange/gold) derived from the logo, conveying energy, authority and international reach.
colors:
  primary: "#8B0000"
  on-primary: "#FFFFFF"
  secondary: "#FF6900"
  on-secondary: "#FFFFFF"
  tertiary: "#FCB900"
  on-tertiary: "#1A1A1A"
  surface: "#FFFFFF"
  on-surface: "#666666"
  on-surface-dark: "#333333"
  border: "#e2e2e2"
  overlay-dark: "rgba(0,0,0,0.62)"
  overlay-light: "rgba(0,0,0,0.17)"
  link: "#2EA3F2"
typography:
  hero-h1:
    fontFamily: Lora
    fontSize: 36px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: 0em
    fontFeature: smcp
  h1:
    fontFamily: Lora
    fontSize: 30px
    fontWeight: 500
    lineHeight: 1.2
    letterSpacing: 0em
  h2:
    fontFamily: "'Work Sans'"
    fontSize: 30px
    fontWeight: 500
    lineHeight: 1.2
    letterSpacing: 0em
  h4-upper:
    fontFamily: "'Work Sans'"
    fontSize: 14px
    fontWeight: 700
    lineHeight: 1
    letterSpacing: 0.1em
    textTransform: uppercase
  body:
    fontFamily: "'Open Sans'"
    fontSize: 14px
    fontWeight: 500
    lineHeight: 1.7
    letterSpacing: 0em
  body-sm:
    fontFamily: "'Open Sans'"
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.6
  button:
    fontFamily: "'Work Sans'"
    fontSize: 14px
    fontWeight: 700
    lineHeight: 1
    letterSpacing: 0.3em
    textTransform: uppercase
rounded:
  none: 0px
  sm: 3px
  md: 0px
spacing:
  unit: 8px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  section-padding: 54px
  row-padding: 27px
components:
  button-primary:
    backgroundColor: "#8B0000"
    textColor: "#FFFFFF"
    typography: "{typography.button}"
    rounded: "{rounded.none}"
    padding: "20px 30px"
  button-accent:
    backgroundColor: "#FF6900"
    textColor: "#FFFFFF"
    typography: "{typography.button}"
    rounded: "{rounded.none}"
    padding: "20px 30px"
  button-gold:
    backgroundColor: "#FCB900"
    textColor: "#1A1A1A"
    typography: "{typography.button}"
    rounded: "{rounded.none}"
    padding: "20px 30px"
  button-link:
    backgroundColor: "transparent"
    textColor: "#8B0000"
    typography: "{typography.button}"
    borderWidth: "2px"
    borderColor: "#8B0000"
    borderStyle: solid
    rounded: "{rounded.none}"
    padding: "0.3em 1em"
  card-clean:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    rounded: "{rounded.none}"
    padding: "{spacing.lg}"
    border: "1px solid {colors.border}"
  card-shadow:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    rounded: "{rounded.none}"
    padding: "{spacing.lg}"
  input-field:
    backgroundColor: "{colors.surface}"
    textColor: "#4e4e4e"
    typography: "{typography.body}"
    border: "1px solid #bbb"
    rounded: "{rounded.none}"
    padding: "2px 4px"
---

## Overview

Élan Forensic es una consultoría de economía y finanzas orientada al arbitraje internacional y el sector energético. La marca transmite autoridad, rigor técnico y alcance global. El tono es institucional y refinado, con una paleta cálida inspirada en los colores del logo (rojo oscuro, naranja, dorado).

El público objetivo son fondos de inversión, firmas legales internacionales, utilities y gobiernos. La personalidad visual combina seriedad corporativa con energía — el nombre "Élan" significa impulso y estilo en francés, y la paleta cálida (rojo/naranja/dorado) refleja ese dinamismo sin perder autoridad.

## Colors

Paleta cálida cálida (Rojo/Naranja/Dorado). Inspirada en el logo corporativo — rojo oscuro como color institucional, naranja para acciones e highlights, dorado para elementos de prestigio y accents.

- **Primary (#8B0000):** Rojo oscuro (dark red) para fondos hero, headers, elementos de autoridad. Transmite tradición, poder institucional. Usado en fondos de secciones clave y como color primario de la marca.
- **Secondary (#FF6900):** Naranja vibrante como color de acción. Botones primarios, CTAs, elementos que requieren atención inmediata. Equivalente funcional al accent pero más enérgico.
- **Tertiary (#FCB900):** Dorado/Amarillo para elementos de prestigio y highlights. usado con moderación — connota excelencia, éxito, calidad premium.
- **Link (#2EA3F2):** Azul para enlaces de navegación dentro del contenido (este es el único color frío, retained from Divi).
- **Surface (#FFFFFF):** Blanco puro para fondos de contenido, cards, áreas de texto.
- **On-Surface (#666666):** Gris medio para texto de cuerpo.
- **On-Surface Dark (#333333):** Casi negro para headlines y títulos de sección.
- **Border (#e2e2e2):** Gris suave para separadores, bordes de cards.
- **Overlay Dark (#000000 @ 62%):** Para overlays sobre imágenes de fondo en secciones hero.

## Typography

Sistema de tres tipografías — Lora (serif, headlines), Work Sans (sans-serif, labels/buttons), Open Sans (body, flexible). Sin cambios respecto a la paleta anterior.

- **Hero H1:** Lora 500, 36px, line-height 1.4 — serif authority para el título principal del hero. Texto blanco sobre imagen de fondo.
- **H2:** Work Sans 500, 30px — títulos de sección. Color #333333.
- **H4 Upper:** Work Sans 700, 14px, uppercase, letter-spacing 0.1em — eyebrows/categorías sobre los headlines.
- **Body:** Open Sans 500, 14px, line-height 1.7 — texto de lectura.
- **Button:** Work Sans 700, 14px, uppercase, letter-spacing 0.3em — CTAs con tracking amplio.

## Layout

Grid de 80% de ancho, max 1080px. Sistema de espaciado basado en 8px. Sin gutters visibles — el espacio blanco es negativo.

- **Container:** 80% width, max 1080px, margin auto
- **Section padding:** 54px top/bottom (desktop)
- **Row padding:** 27px
- **Responsive breakpoints:** 980px (tablet), 767px (mobile)
- **Cards:** padding 24px, bordes limpios

El layout es limpio y editorial. No hay ornamento. El espacio negativo es load-bearing.

## Elevation & Depth

Diseño mayormente plano con sombras sutiles solo en interacciones.

- **Cards clean:** Fondo blanco, borde 1px en #e2e2e2 — sin sombra.
- **Portfolio hover:** Scale 1.08x sobre imagen, overlay oscuro rgba(0,0,0,0.35) aparece sobre la imagen.
- **Fixed header:** Background white semi-transparente (88% opacity) con blur — semi-transparente.
- **Botones:** Sin border-radius (0px) — formas rectas, arquitectónicas.
- **Botón hover:** Border transparente, padding se expande de 0.7em a 2em en el lado derecho.

## Shapes

Lenguaje de formas angulares y minimalistas. Sin redondeo en elementos UI.

- **Border-radius 0px** en todos los elementos interactivos — botón, cards, inputs. Sharp, engineered.
- **Excepción:** border-radius 3px en elementos menores (footer info, badges).

## Components

### Botón primario (Primary CTA)
Background #8B0000 (rojo oscuro), texto blanco, Work Sans uppercase. Para acciones principales en fondos claros.

### Botón accent (Secondary CTA)
Background #FF6900 (naranja), texto blanco. Para acciones de alto contraste en fondos blancos.

### Botón dorado (Prestige CTA)
Background #FCB900 (dorado), texto oscuro (#1A1A1A). Para acciones premium o secciones especiales.

### Botón link
Sin fill, borde 2px en #8B0000, texto rojo oscuro. Para navegación secundaria.

### Portfolio cards
Grid 2 columnas (desktop), 1 columna (mobile). Aspect-ratio 16:9. Imagen cover con scale hover (1.08x). Overlay oscuro aparece en hover con título en blanco centrado.

### Header fijo
Background white semi-transparente (88% opacity) con blur. Navegación dark con alto contraste.

### Cards de texto
Limpias, fondo blanco, padding 24px, borde 1px en #e2e2e2. Sin sombras.

## Do's and Don'ts

- **Do** usar Lora para headlines que requieran autoridad y sofisticación.
- **Do** usar Work Sans uppercase para labels, categorías y CTAs.
- **Do** mantener el naranja (#FF6900) para acciones e interactividad — es el color de energía.
- **Do** usar el dorado (#FCB900) con moderación — es para prestige, no para bulk.
- **Don't** usar border-radius en elementos de UI primarios.
- **Don't** usar más de 2 weights tipográficos en la misma vista.
- **Don't** colocar texto body directamente sobre fondos primary (#8B0000) sin ajustar a blanco.
- **Don't** usar naranja o dorado para elementos de navegación o estructura — es para acción.
- **Don't** usar el rojo primario para fondos大面积 — es un color pesado, mejor en elementos focalizados.