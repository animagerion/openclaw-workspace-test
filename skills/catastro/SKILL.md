---
name: catastro
description: Consulta datos catastrales de España por dirección. Genera informes y los sube a Google Docs.
---

# Catastro — Datos Catastrales de España

Consulta información catastral de inmuebles usando la API oficial del Catastro (ovc.catastro.meh.es). No requiere certificado ni API key — es gratuito para datos no protegidos.

## Ubicación

CLI: `/home/gerion/.local/bin/catastro`
Script: `/home/gerion/.openclaw/workspace/scripts/catastro_cli.py`

## Uso rápido

```bash
catastro <provincia> <municipio> <calle> [numero]
```

## Ejemplos

```bash
# Consulta básica
catastro Sevilla Utrera "Forcadell" 8
catastro Cadiz Rota "Marina" 1

# Con параметры опциональные
catastro Sevilla "Gorri" 14 --sigla CL
catastro Cadiz Rota "Playa" 5 --json
```

## Datos que devuelve

- **Referencia Catastral** (20 caracteres)
- **Dirección completa**
- **Uso** (Residencial, Almacén, etc.)
- **Superficie construida total** (m²)
- **Año de construcción**
- **Distribución por plantas** (cada uso con sus m²)

## Campos que NO devuelve la API gratuita

La API devuelve `bico` pero NO incluye el campo `finca` con `<ss>` (superficie del solar). Esto es así aunque la documentación lo menciona — el servidor en producción no lo está devolviendo actualmente. Para ese dato se necesita:
- Acceso con certificado digital o Cl@ve
- API de terceros (catastro-api.es)

## Para generar informe y subir a Google Docs

```python
# 1. Ejecutar consulta
result = subprocess.run(
    ['catastro', 'Sevilla', 'Utrera', 'Forcadell', '8'],
    capture_output=True, text=True
)
informe = result.stdout

# 2. Crear documento en Google Docs
subprocess.run(['gog', 'docs', 'create', 'Informe Catastral - Forcadell 8'])

# 3. Escribir contenido
subprocess.run(['gog', 'docs', 'write', '<DOC_ID>', '--file', '/tmp/informe.txt', '--append'])

# 4. Compartir
subprocess.run(['gog', 'docs', 'share', '<DOC_ID>', '--email', 'paduel@gmail.com', '--role', 'reader'])
```

## Enviar por email con adjunto gráfico

```python
# Generar gráfico si es un ticker financiero
# Subir a Drive
subprocess.run(['gog', 'drive', 'upload', '/tmp/grafico.png', '--name', 'grafico.png'])
# Adjuntar en email
subprocess.run(['gog', 'mail', 'send', '--to', 'paduel@gmail.com', '--subject', '...', '--attach', '/tmp/grafico.png'])
```

## Notas técnicas

- API: `https://ovc.catastro.meh.es/ovcservweb/OVCSWLocalizacionRC/OVCCallejero.asmx`
- Métodos disponibles: Consulta_DNPLOC, Consulta_DNPRC, Consulta_DNPPP, ConsultaVia
- La búsqueda de calle ajusta automáticamente el nombre al encontrar coincidencias en el callejero
- Si el número no existe, devuelve lista de candidatos
