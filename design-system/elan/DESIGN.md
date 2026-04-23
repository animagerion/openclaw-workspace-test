---
version: alpha
name: Élan Forensic
description: Corporate legal and forensic consultancy brand. Authoritative, precise, and internationally focused.
colors:
  primary: "#002255"
  on-primary: "#FFFFFF"
  accent: "#00D084"
  on-accent: "#FFFFFF"
  link: "#2EA3F2"
  surface: "#FFFFFF"
  on-surface: "#666666"
  on-surface-dark: "#333333"
  border: "#e2e2e2"
  overlay-dark: "rgba(0,0,0,0.62)"
  overlay-light: "rgba(0,0,0,0.17)"
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
    backgroundColor: "#FFFFFF"
    textColor: "#000000"
    typography: "{typography.button}"
    rounded: "{rounded.none}"
    padding: "20px 30px"
  button-accent:
    backgroundColor: "#00D084"
    textColor: "#FFFFFF"
    typography: "{typography.button}"
    rounded: "{rounded.none}"
    padding: "20px 30px"
  button-link:
    backgroundColor: "transparent"
    textColor: "#000000"
    typography: "{typography.button}"
    borderWidth: "2px"
    borderColor: "#000000"
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

Élan Forensic es una consultoría de economía y finanzas orientada al arbitraje internacional y el sector energético. La marca transmite autoridad, rigor técnico y alcance global. El tono es institucional y refinado, sin ser frío. El público objetivo son fondos de inversión, firmas legales internacionales, utilities y gobiernos.

La personalidad visual combina seriedad corporativa con un toque de dinamismo (el nombre "Élan" significa impulso, estilo en francés). El color verdeaccent (#00D084) rompe con la paleta naval más conservadora y aporta energía.

## Colors

Paleta Naval + Verde Accent. El azul transmite confianza institucional y prestigio. El verde accent es la señal de energía y acción — usado solo en elementos que requieren atención (CTAs, highlights, el logo dot).

- **Primary (#002255):** Azul naval profundo para fondos hero, headers, elementos de autoridad. Usado en backgrounds de secciones clave y en el logo corporativo.
- **Accent (#00D084):** Verde esmeralda vibrante como color de acción. Botones primarios, destacados, el punto en el logo. Usado con moderación — es un acento, no un color de fondo principal.
- **Link (#2EA3F2):** Azul claro para enlaces y navegación dentro del contenido.
- **Surface (#FFFFFF):** Blanco puro para fondos de contenido, cards, areas de texto.
- **On-Surface (#666666):** Gris medio para texto de cuerpo — ni negro puro ni gris claro. Se mueve bien sobre fondo blanco.
- **On-Surface Dark (#333333):** Casi negro para headlines y títulos de sección.
- **Border (#e2e2e2):** Gris suave para separadores, bordes de cards, elementos estructurales.
- **Overlay Dark (#000000 @ 62%):** Para overlays sobre imágenes de fondo en secciones hero.

## Typography

Sistema de tres tipografías — Lora (serif, headlines), Work Sans (sans-serif, labels/buttons), Open Sans (body, flexible).

- **Hero H1:** Lora 500, 36px, line-height 1.4 — serif authority para el título principal del hero. Texto blanco sobre imagen de fondo.
- **H2:** Work Sans 500, 30px — títulos de sección. Color #333333.
- **H4 Upper:** Work Sans 700, 14px, uppercase, letter-spacing 0.1em — eyebrows/categorías sobre los headlines. Labels pequeños de sección.
- **Body:** Open Sans 500, 14px, line-height 1.7 — texto de lectura. Máximo contraste en paragraphs: padding-bottom 1em.
- **Button:** Work Sans 700, 14px, uppercase, letter-spacing 0.3em — CTAs. Tracking amplio (0.3em) para autoridad.

No se mezcla font-weight dentro del mismo elemento. Los itálicos (Open Sans) se usan solo para énfasis en texto de cuerpo.

## Layout

Grid de 80% de ancho, max 1080px. Sistema de espaciado basado en 8px. Sin gutters visibles en la estructura — el espacio blanco es negativo.

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
- **Fixed header:** Background rgba(255,255,255,0.88) con blur backdrop — semi-transparente.
- **Botones:** Sin border-radius (0px) — formas rectas, arquitectónicas.
- **Botón hover:** Border transparente, padding se expande de 0.7em a 2em en el lado derecho.

## Shapes

Lenguaje de formas angulares y minimalistas. Sin redondeo en elementos UI.

- **Border-radius 0px** en todos los elementos interactivos — botón, cards, inputs. Sharp, engineered.
- **Excepción:** border-radius 3px en elementos menores (footer info, badges).

## Components

### Botón primario
Estilo: White background, texto negro, letra amplia, sin borde, sin radio. Padding generoso 20px 30px.

### Botón accent (CTA principal)
Estilo: Background #00D084, texto blanco, Work Sans uppercase. Solo para acciones más importantes de cada sección.

### Portfolio cards
Grid 2 columnas (desktop), 1 columna (mobile). Aspect-ratio 16:9. Imagen cover con scale hover (1.08x). Overlay oscuro aparece en hover con título en blanco centrado.

### Header fijo
Background white semi-transparente (88% opacity) con blur. Navegación dark con alto contraste.

### Cards de texto
Limpias, fondo blanco, padding 24px, borde 1px en #e2e2e2. Sin sombras.

### Inputs
Borde 1px #bbb, sin radio, padding 2px. Focus: borde #2d3940.

## Do's and Don'ts

- **Do** usar Lora para headlines que requieran autoridad y sofisticación.
- **Do** usar Work Sans uppercase para labels, categorías y CTAs.
- **Do** mantener los acentos verdes (#00D084) para acciones y highlights — no usar como color de fondo大面积.
- **Don't** usar border-radius en elementos de UI primarios.
- **Don't** usar más de 2 weights tipográficos en la misma vista.
- **Don't** colocar texto body directamente sobre fondos primary (#002255) sin ajustar a blanco.
- **Don't** usar el verde accent para elementos de navegación o estructura — es para acción.
- **Don't** usar Open Sans italic para headlines — es para énfasis dentro de párrafos.